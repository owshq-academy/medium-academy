from datetime import datetime
from src.producer.producer_json import KafkaJson

# Sample message data (could be a dict, list of dicts, or a string)
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

# Kafka topic and broker details
kafka_topic = "user_activity"
broker = "localhost:9094"
client_id = "python_client_json"

# Initialize the KafkaJson producer
kafka_json_producer = KafkaJson(broker=broker, auth=False)

# Produce JSON messages to Kafka
# Optional arguments: batch_size, max_workers, additional_config
kafka_json_producer.json_producer(
    object_name=message_data,           # Can be a dict, list of dicts, or a string
    kafka_topic=kafka_topic,            # Kafka topic to send messages to
    client_id=client_id,                # Client ID for the Kafka producer
    batch_size=2,                       # Number of messages to send per batch
    max_workers=2                       # Number of threads to process batches
)