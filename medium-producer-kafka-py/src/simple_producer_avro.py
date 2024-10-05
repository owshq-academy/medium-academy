from datetime import datetime
from src.producer.producer_avro import KafkaAvroProducer

# Sample data to be sent to Kafka
message_data = [
    {
        "id": 1,
        "name": "Mateus",
        "age": 37,
        "created_at": datetime.now(),
        "event": "login"
    },
    {
        "id": 2,
        "name": "Luan",
        "age": 35,
        "created_at": datetime.now(),
        "event": "logout"
    },
    {
        "id": 3,
        "name": "Leonardo",
        "age": 42,
        "created_at": datetime.now(),
        "event": "purchase",
        "amount": 250.5
    }
]

# Paths to the Avro schemas for key and value
schema_key_path = 'schemas/s_key_user_activity.json'
schema_value_path = 'schemas/s_value_user_activity.json'

# Kafka broker and Schema Registry configuration
broker = "localhost:9094"
schema_registry_url = "http://localhost:8081"
client_id = "python_client_json_avro"

# Initialize the KafkaAvroProducer
kafka_producer = KafkaAvroProducer(broker=broker, schema_registry_url=schema_registry_url, max_workers=4)

# Produce the messages to Kafka topic 'user_activity'
kafka_producer.avro_producer(
    object_list=message_data,                # List of messages to be sent
    kafka_topic="user_activity_avro",        # Kafka topic name
    schema_key_path=schema_key_path,         # Path to the key schema
    schema_value_path=schema_value_path,     # Path to the value schema
    batch_size=2,                            # Number of messages to send per batch
    kafka_client_id_avro=client_id           # Client Application name
)