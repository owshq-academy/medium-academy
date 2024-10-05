import json
import logging
from confluent_kafka import Producer, KafkaException
from datetime import datetime
from src.producer.producer_settings import producer_settings_json
from src.producer.delivery_reports import on_delivery_json
from concurrent.futures import ThreadPoolExecutor
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KafkaJson(object):
    def __init__(self, broker, auth=False):
        self.broker = broker
        self.auth = auth

    def json_producer(self, object_name, kafka_topic, client_id, additional_config=None, batch_size=100, max_workers=4):
        # Choose auth settings and merge with additional config
        base_config = producer_settings_json(self.broker) if self.auth else producer_settings_json(self.broker, client_id)
        if additional_config:
            base_config.update(additional_config)

        try:
            p = Producer(base_config)
        except KafkaException as e:
            logging.error(f"Failed to create Kafka producer: {e}")
            return

        # Data preparation
        get_data = self._prepare_data(object_name)
        if not get_data:
            logging.error("Error: Invalid format for object_name.")
            return

        # Split data into partitions for parallel processing
        partition_size = max(1, len(get_data) // max_workers)  # Handle cases with fewer items
        partitions = [get_data[i:i + partition_size] for i in range(0, len(get_data), partition_size)]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for partition in partitions:
                executor.submit(self._produce_batch, p, partition, kafka_topic, batch_size)

        p.flush()
        logging.info("All messages have been flushed to Kafka.")

    def _prepare_data(self, object_name):
        if isinstance(object_name, dict):
            return [object_name]
        elif isinstance(object_name, str):
            return [{"message": object_name}]
        elif isinstance(object_name, list) and all(isinstance(item, dict) for item in object_name):
            return object_name
        return None

    def _produce_batch(self, producer, batch, topic, batch_size):
        temp_batch = []
        for data in batch:
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()

            temp_batch.append(data)

            if len(temp_batch) >= batch_size:
                self._send_batch(producer, temp_batch, topic)
                temp_batch.clear()

        if temp_batch:
            self._send_batch(producer, temp_batch, topic)

        producer.poll(0)

    def _send_batch(self, producer, batch, topic, retries=3):
        for data in batch:
            id_value = data.get("id")
            success = False
            attempt = 0

            while not success and attempt < retries:
                try:
                    producer.produce(
                        topic=topic,
                        key=json.dumps(id_value).encode('utf-8') if id_value else None,
                        value=json.dumps(data).encode('utf-8'),
                        callback=on_delivery_json
                    )
                    success = True
                except BufferError:
                    logging.warning("Producer buffer is full; retrying after 0.1s.")
                    producer.poll(0.1)
                    time.sleep(0.1)
                except KafkaException as e:
                    logging.error(f"Kafka error: {e}")
                    attempt += 1
                    time.sleep(2 ** attempt)  # Exponential backoff
                except ValueError as e:
                    logging.error(f"Invalid input: {e}")
                    break
                except KeyboardInterrupt:
                    logging.info("Producer interrupted by user.")
                    return

        producer.poll(0)