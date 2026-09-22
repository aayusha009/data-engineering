## week 10 kafka-streaming

This is a simple hands on demo of Apache Kafka.

I used Docker to run a Kafka broker on my laptop. I created a topic called orders, then wrote a producer script that sends a few sample messages into it, and a consumer script that reads those messages back out.

I also made a second topic called orders_multi with three partitions instead of one, to see how partitioning changes things. With one partition, messages came back in the exact order sent. With three partitions, they came back in a different order, since Kafka only guarantees order within a single partition, not across the whole topic.

To run it, start Docker Desktop, run docker compose up -d to start Kafka, then run python3 producer.py followed by python3 consumer.py.

This helped me understand how topics, partitions, producers, and consumers actually work together in a real Kafka setup.