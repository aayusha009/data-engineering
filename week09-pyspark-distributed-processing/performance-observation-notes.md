## Performance Observations

I ran this pipeline on about 3.5 million taxi trips using PySpark locally, using all the CPU cores on my laptop.

For the join, I used a broadcast join since the zone lookup table was small. This let Spark copy that small table to every worker instead of shuffling the much bigger trips table, which saved a lot of unnecessary work.

The aggregate step, grouping trips by date and borough, did cause a shuffle. I checked the Spark UI at localhost:4040 and saw the aggregate stage had 555.8 KiB of input and 35.0 KiB of shuffle write, meaning Spark had to rewrite that much data to complete the grouping.

The read, clean, and join steps all ran fast since they didn't need a shuffle. The aggregate step was the only one that caused real data movement.