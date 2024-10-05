import json
import logging
import time
from confluent_kafka import Producer, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from datetime import datetime
from src.producer.producer_settings import producer_settings_avro
from src.producer.delivery_reports import on_delivery_avro
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KafkaAvroProducer:
    def __init__(self, broker, schema_registry_url, auth=False, max_workers=4):
        self.broker = broker
        self.schema_registry_url = schema_registry_url
        self.auth = auth
        self.max_workers = max_workers

    @staticmethod
    def load_json_schema(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError as e:
            logger.error(f"File not found: {file_path}")
            raise e
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in file {file_path}: {e}")
            raise e

    def avro_producer(self, object_list, kafka_topic, schema_key_path, kafka_client_id_avro, schema_value_path, additional_config=None, batch_size=100):
        schema_key = self.load_json_schema(schema_key_path)
        schema_value = self.load_json_schema(schema_value_path)

        schema_registry_conf = {'url': self.schema_registry_url}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        base_config = producer_settings_avro(self.broker, kafka_client_id_avro)
        if additional_config:
            base_config.update(additional_config)

        try:
            avro_serializer_key = AvroSerializer(schema_str=json.dumps(schema_key), schema_registry_client=schema_registry_client)
            avro_serializer_value = AvroSerializer(schema_str=json.dumps(schema_value), schema_registry_client=schema_registry_client)
            producer = Producer(base_config)
        except Exception as e:
            logger.error(f"Failed to initialize serializers or producer: {e}")
            return

        if not isinstance(object_list, list):
            object_list = [object_list]

        partition_size = max(1, len(object_list) // self.max_workers)  # Avoid empty partitions
        partitions = [object_list[i:i + partition_size] for i in range(0, len(object_list), partition_size)]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._produce_batch, producer, partition, kafka_topic, avro_serializer_key, avro_serializer_value, batch_size) for partition in partitions]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error in batch processing: {e}")

        producer.flush()
        logger.info("All messages have been flushed to Kafka.")

    def _produce_batch(self, producer, batch, topic, avro_serializer_key, avro_serializer_value, batch_size):
        temp_batch = []
        for data in batch:
            # Ensure proper serialization of datetime objects
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()

            temp_batch.append(data)

            if len(temp_batch) >= batch_size:
                self._send_batch(producer, temp_batch, topic, avro_serializer_key, avro_serializer_value)
                temp_batch.clear()

        if temp_batch:
            self._send_batch(producer, temp_batch, topic, avro_serializer_key, avro_serializer_value)

        producer.poll(0)

    def _send_batch(self, producer, batch, topic, avro_serializer_key, avro_serializer_value, retries=3):
        for data in batch:
            id_value = data.get("id")
            if id_value is None:
                logger.error(f"No 'id' field found in data: {data}")
                continue

            success = False
            attempt = 0

            while not success and attempt < retries:
                try:
                    producer.produce(
                        topic=topic,
                        key=avro_serializer_key({'id': id_value}, SerializationContext(topic, MessageField.KEY)),
                        value=avro_serializer_value(data, SerializationContext(topic, MessageField.VALUE)),
                        on_delivery=lambda err, msg: on_delivery_avro(err, msg, data)
                    )
                    success = True
                except BufferError:
                    logger.warning("Producer buffer is full; retrying after 0.1s.")
                    producer.poll(0.1)
                    time.sleep(0.1)
                except KafkaException as e:
                    logger.error(f"Kafka exception on produce: {e}")
                    attempt += 1
                    time.sleep(2 ** attempt)  # Exponential backoff
                except Exception as e:
                    logger.error(f"Failed to produce message: {e}")
                    break

        producer.poll(0)