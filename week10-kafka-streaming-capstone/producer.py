# import the tool that lets Python send messages to Kafka
from kafka import KafkaProducer
# import time so we can pause between messages
import time

# connect to the Kafka broker running on our machine
producer = KafkaProducer(bootstrap_servers="localhost:9092")

# a list of pretend order messages to send
orders = ["order #1 placed", "order #2 placed", "order #3 placed"]

# loop through each message one at a time
for order in orders:
    # send the message into the "orders" topic
    # .encode() turns the text into bytes, which Kafka requires
    producer.send("orders_multi", order.encode())    # print to our own screen so we can see what was sent
    print("Sent:", order)
    # wait 1 second before sending the next one
    time.sleep(1)

# make sure all messages are actually sent before the script ends
producer.flush()
print("Done sending messages.")