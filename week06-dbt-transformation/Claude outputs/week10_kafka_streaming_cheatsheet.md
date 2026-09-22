# Week 10 Cheat Sheet — Kafka, Streaming, CDC

**Batch vs Streaming vs Micro-batch**
- Batch = collect data, process it all later in one go (like laundry once a week).
- Streaming = process each event the instant it arrives (like washing a dish right after use).
- Micro-batch = middle ground — process in small chunks every few seconds/minutes.

**Kafka core parts**
- Broker = a server that stores and passes along messages.
- Topic = a named category messages go into (e.g. "orders").
- Partition = splits a topic into parallel lanes so multiple things can read/write at once.
- Producer = sends messages into a topic.
- Consumer = reads messages out of a topic.

**Offset** — a message's position number in a partition, so Kafka always knows where reading left off.

**Consumer group** — a team of consumers that split up a topic's partitions between them (no duplicate work); if one consumer dies, the others take over its partitions.

**Delivery semantics**
- At-most-once = might lose a message, never duplicates it.
- At-least-once = never loses a message, might duplicate it.
- Exactly-once = never lost, never duplicated — the ideal, but hardest to build. Most real systems use at-least-once + dedupe logic.

**Schema management (Avro/Protobuf)** — a strict, compact format producers and consumers both agree on, so data always arrives in the expected shape, and can evolve safely over time. (Just need awareness, not implementation.)

**CDC + Debezium**
- CDC (Change Data Capture) = watches a database's internal change log and emits an event for every insert/update/delete, instead of repeatedly polling.
- Debezium = a popular tool that does this, usually paired with Kafka.

**Lambda architecture** — run a batch pipeline (accurate, slower) and a streaming pipeline (fast, less complete) side by side, then merge the results.

**Kappa architecture** — simpler alternative: just one streaming pipeline; to "redo" history, replay the stream from the start.

**When streaming is the wrong choice** — streaming adds real complexity (harder to debug/test). Only worth it if you truly need near real-time results. If daily/hourly batch is fast enough, use batch — don't over-engineer.
