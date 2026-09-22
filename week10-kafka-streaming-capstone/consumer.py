# import the tool that lets Python receive messages from Kafka
from kafka import KafkaConsumer

# connect to the Kafka broker and listen to the "orders" topic
consumer = KafkaConsumer(
    "orders_multi",
    bootstrap_servers="localhost:9092",
    # start reading from the very first message ever sent, not just new ones
    auto_offset_reset="earliest",
    # stop automatically if no new messages arrive for 5 seconds (just for this demo)
    consumer_timeout_ms=5000
)

print("Listening for messages...")

# loop through every message this consumer receives
for message in consumer:
    # .decode() turns the raw bytes back into readable text
    print("Received:", message.value.decode(), "| Partition:", message.partition)
print("No more messages. Consumer stopped.")