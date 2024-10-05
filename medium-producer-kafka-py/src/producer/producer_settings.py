# Optimized JSON producer settings
def producer_settings_json(broker, client_id):
    return {
        'bootstrap.servers': broker,
        'client.id': client_id,
        'compression.type': 'gzip',  # Compress messages to save bandwidth
        'batch.size': 65536,  # Double the batch size to improve throughput
        'linger.ms': 50,  # Allow more time for messages to batch, improving efficiency
        'queue.buffering.max.messages': 100000,  # Max messages in the queue
        'queue.buffering.max.ms': 500,  # Max time before sending a batch
        'acks': 'all',  # Ensure all replicas acknowledge the message for reliability
        'retries': 10,  # Increase retries to handle transient failures
        'retry.backoff.ms': 200,  # Increase backoff to avoid overwhelming broker
        'enable.idempotence': True,  # Ensures exactly-once delivery in case of retries
        'max.in.flight.requests.per.connection': 5,  # Allow up to 5 in-flight requests for higher throughput
        'delivery.timeout.ms': 30000,  # Set a delivery timeout
        'request.timeout.ms': 30000  # Set request timeout
    }

# Optimized Avro producer settings
def producer_settings_avro(broker, client_id_avro):
    return {
        'bootstrap.servers': broker,
        'client.id': client_id_avro,
        'acks': "all",  # Ensure strong delivery guarantees (all replicas must acknowledge)
        'enable.idempotence': True,  # Ensures exactly-once delivery
        'compression.type': 'gzip',  # Gzip compression to reduce payload size
        'batch.size': 65536,  # Increased batch size for better throughput
        'linger.ms': 50,  # Slightly higher to allow batching of more messages
        'queue.buffering.max.messages': 100000,  # Max messages in queue for buffering
        'queue.buffering.max.ms': 500,  # Maximum time to wait before sending a batch
        'max.in.flight.requests.per.connection': 5,  # Allow more requests for higher throughput, but avoid out-of-order issues
        'retries': 10,  # Retry up to 10 times on failure
        'retry.backoff.ms': 200,  # Backoff time between retries
        'delivery.timeout.ms': 30000,  # Timeout for message delivery
        'request.timeout.ms': 30000,  # Timeout for request handling
        'message.max.bytes': 5000000,  # Allow larger messages, default is 1MB, increased to 5MB
        'receive.message.max.bytes': 5000000  # Set maximum size of a message that the broker can receive
    }