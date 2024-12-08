from confluent_kafka import Producer, Consumer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
import sys

# Kafka configuration
KAFKA_BROKERS = 'localhost:9093,localhost:9093,localhost:9094'
TOPIC_NAME = 'test'
NUM_PARTITIONS = 10
REPLICATION_FACTOR = 3



# Configure the Kafka Admin client
def create_kafka_topic():
    # Create an Admin client to interact with the Kafka cluster
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKERS})

    # Kafka topic creation configuration
    topic_config = {
        'num.partitions': NUM_PARTITIONS,
        'replication.factor': REPLICATION_FACTOR,
    }

    try:
        fs = admin_client.create_topics(
            [NewTopic(TOPIC_NAME, NUM_PARTITIONS, REPLICATION_FACTOR)],
            operation_timeout=30
        )
        fs[TOPIC_NAME].result()  # Wait for the topic creation to complete
        print(f"Topic {TOPIC_NAME} created successfully.")

    except KafkaException as e:
        print(f"Error creating topic: {e}")
        sys.exit(1)


# Configure the Kafka producer
def create_producer():
    # Producer configuration
    producer_conf = {
        'bootstrap.servers': KAFKA_BROKERS,
        'acks': 'all',  # Ensure all replicas acknowledge the message
        'retries': 3,  # Retry in case of failure
        'linger.ms': 10,  # Reduce latency
        'batch.size': 16384  # The maximum size (in bytes) of a batch of records that the producer will attempt to send to a single partition in one request.
    }

    # Create the producer instance
    producer = Producer(producer_conf)
    print("created producer")
    return producer


def delivery_report(err, msg):
    if err:
        print(f'Error while trying to send the message: {err}')
    else:
        print(f'message successfully received on kafka brokers: {msg.value()}, partition: {msg.partition()}')



# Produce messages to the topic
def produce_messages(producer):
    try:
        for i in range(1000):  # Sending 10 messages
            message = f"Message {i + 1}"
            producer.produce(TOPIC_NAME, message, callback=delivery_report)
            producer.poll(0.1)  # Ensure the message is sent asynchronously
            print("produced messages async to the queue")
        producer.flush()  # Wait for all messages to be sent
        print("messages flushed to brokers")

    except KafkaException as e:
        print(f"Error producing message: {e}")
        sys.exit(1)


# Configure the Kafka consumer
def create_consumer():
    # Consumer configuration
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKERS,
        'group.id': 1,
        'auto.offset.reset': 'earliest',  # Start consuming from the beginning if no offset exists
    }

    # Create the consumer instance
    consumer = Consumer(consumer_conf)
    consumer.subscribe([TOPIC_NAME])  # Subscribe to the topic
    print("created consumer")
    return consumer


# Consume messages from the topic
def consume_messages(consumer):
    try:
        print(f"Consuming messages from {TOPIC_NAME}...")
        while True:

            msg = consumer.poll(timeout=1.0)  # Adjust the timeout as needed

            if msg is None:
                continue  # No message available within the timeout

            if msg.error():
                raise KafkaException(msg.error())

            else:
                print(f"Consumed message: {msg.value().decode('utf-8')}", flush=True)

    except KeyboardInterrupt:
        print("Consuming stopped.")
    finally:
        consumer.close()  # Clean up and close the consumer


# Main function to configure Kafka topic, produce and consume messages
def main():
    #create_kafka_topic()  # Step 1: Create topic with 10 partitions and replication factor 2

    # Step 2: Set up producer and send messages
    producer = create_producer()
    produce_messages(producer)

    # Step 3: Set up consumer and consume messages
    consumer = create_consumer()
    consume_messages(consumer)


if __name__ == '__main__':
    main()
