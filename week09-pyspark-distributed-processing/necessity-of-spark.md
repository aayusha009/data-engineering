## Write notes on whether Spark was necessary for the dataset

For this specific dataset of about 3.5 million rows, a tool like pandas could probably have handled it on a modern laptop, though it would likely be slower and use more memory since pandas loads everything into memory at once.

Spark was still useful here because it processes data in a distributed way, even on a single laptop, splitting the work across all available CPU cores. This made operations like the join and aggregate faster and more memory efficient than they might have been otherwise.

If this dataset grew much larger, for example covering a full year or multiple years of trip data instead of just one month, Spark would become necessary rather than just helpful, since that amount of data would be too large for a single machine's memory to handle with a tool like pandas.

So for this exercise, Spark was a reasonable choice to demonstrate distributed processing concepts, but not strictly required at this exact data size.