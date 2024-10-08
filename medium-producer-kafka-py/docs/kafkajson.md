# KafkaJson Class Documentation

This document explains the implementation and functionality of the KafkaJson class, which is designed to send JSON messages to a Kafka topic using the confluent_kafka.Producer and handle message delivery in batches. Below is an overview of the class’s key components and methods.

### Class Overview

The KafkaJson class is responsible for producing JSON messages to a Kafka topic. It allows for batch processing and parallelization using a thread pool. The class handles authentication settings, data preparation, message production, and error handling during the message delivery process.

Dependencies

	•	json: For encoding Python objects into JSON format.
	•	logging: To log messages, including errors and informational outputs.
	•	confluent_kafka.Producer: To produce messages to a Kafka topic.
	•	KafkaException: To handle Kafka-specific exceptions.
	•	ThreadPoolExecutor: To manage concurrent execution for batch processing.
	•	datetime: For working with date and time in the JSON messages.
	•	producer_settings_json: A function to retrieve producer settings.
	•	on_delivery_json: A callback function to handle the delivery report for each message.
	•	time: To handle retries and time-based operations.

### Initialization

def __init__(self, broker, auth=False):
    self.broker = broker
    self.auth = auth

	•	broker: The Kafka broker address.
	•	auth: A boolean flag indicating whether authentication is required.

### json_producer Method

The json_producer method is responsible for configuring the Kafka producer, preparing the data, and sending messages to the Kafka topic in batches using parallel execution.

def json_producer(self, object_name, kafka_topic, client_id, additional_config=None, batch_size=100, max_workers=4):
    # Auth settings and configuration
    # Creates Kafka producer
    # Prepares data and sends messages in batches using parallel processing

	•	Parameters:
	•	object_name: The data to be sent to Kafka, either a string, a dictionary, or a list of dictionaries.
	•	kafka_topic: The Kafka topic to which the messages will be sent.
	•	client_id: Client identifier used if authentication is not enabled.
	•	additional_config: Additional configuration settings for the Kafka producer.
	•	batch_size: The number of messages to send in each batch.
	•	max_workers: The number of worker threads for parallel execution.
	•	Functionality:
	•	The method sets the appropriate producer configuration, initializes the producer, prepares the data, and divides it into partitions for parallel processing.
	•	It uses ThreadPoolExecutor to execute the message delivery concurrently.
	•	The producer flushes all messages to Kafka after sending.

### _prepare_data Method

This method prepares the data for message production by converting it into the required format.

def _prepare_data(self, object_name):
    # Checks the type of object_name and formats it accordingly

	•	Parameters:
	•	object_name: The data to be formatted (string, dictionary, or list of dictionaries).
	•	Returns:
	•	A list of dictionaries representing the formatted data.

### _produce_batch Method

The _produce_batch method sends a batch of messages to the Kafka topic. It ensures that the data is partitioned into smaller batches and processed in parallel.

def _produce_batch(self, producer, batch, topic, batch_size):
    # Sends messages to Kafka in batches

	•	Parameters:
	•	producer: The Kafka producer instance.
	•	batch: A batch of data to be sent to Kafka.
	•	topic: The Kafka topic.
	•	batch_size: The size of each batch of messages.
	•	Functionality:
	•	The method processes the batch of data, converting any datetime objects into ISO format.
	•	It sends the messages to Kafka in chunks based on the specified batch_size.

### _send_batch Method

This method handles the actual sending of a batch of messages to Kafka, with retries for error handling.

def _send_batch(self, producer, batch, topic, retries=3):
    # Sends each message to Kafka and handles retries for failed messages

	•	Parameters:
	•	producer: The Kafka producer instance.
	•	batch: A list of data to send to Kafka.
	•	topic: The Kafka topic.
	•	retries: The number of retry attempts for each message in case of failure.
	•	Functionality:
	•	The method attempts to send each message in the batch.
	•	It handles common errors such as buffer overflow and Kafka-specific exceptions with retries and exponential backoff.
	•	The method supports user interruption via KeyboardInterrupt.

### Logging

The class uses the logging module to log various events, such as:

	•	Info messages to indicate when messages have been flushed or sent.
	•	Error messages to log failures during Kafka producer initialization or message sending.
	•	Warnings for retry attempts due to buffer overflow.

### Usage Example

```shell
kafka_producer = KafkaJson(broker="localhost:9092", auth=False)
data = {"id": 1, "name": "example", "timestamp": datetime.now()}
kafka_producer.json_producer(object_name=data, kafka_topic="my_topic", client_id="my_client")
```
This example demonstrates how to initialize the KafkaJson class and produce a JSON message to a Kafka topic.