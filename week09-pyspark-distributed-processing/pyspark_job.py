# import the tool that helps to start Spark
from pyspark.sql import SparkSession
# import the tool that helps in refering to a column by name
from pyspark.sql.functions import col, broadcast

# turn Spark on, give it a name, use all cores on this laptop
spark = SparkSession.builder \
    .appName("week9_pyspark_job") \
    .master("local[*]") \
    .getOrCreate()

# READ 

# load the big taxi trips file into a table called "trips"
trips = spark.read.parquet("data/yellow-tripdata.parquet")
# load the small zone lookup file into a table called "zones"
zones = spark.read.csv("data/lookup-table.csv", header=True, inferSchema=True)

# print the column names and types of trips
trips.printSchema()
# print how many rows trips has
print("Row count:", trips.count())

# print the column names and types of zones
zones.printSchema()
# print the first 5 rows of zones so we can see what it looks like
zones.show(5)

# ---- CLEAN ----

# print how many rows trips has before we remove anything
print("Trips BEFORE cleaning:", trips.count())

# start from trips, remove rows missing pickup time or location info
trips_clean = trips.dropna(subset=["tpep_pickup_datetime", "PULocationID", "DOLocationID"]) \
    .filter(col("trip_distance") > 0) \
    .filter(col("fare_amount") > 0)
    # keep only rows where the trip distance is more than 0
    # keep only rows where the fare is more than 0

# print how many rows are left after cleaning
print("Trips AFTER cleaning:", trips_clean.count())

# JOIN

# match each cleaned trip to its pickup zone, using the small zones table
trips_with_zone = trips_clean.join(
    broadcast(zones),
    # match rows where the trip's pickup location ID equals the zone's ID
    trips_clean.PULocationID == zones.LocationID,
    # keep every trip even if no matching zone is found
    "left"
).select(
    # keep every column that trips_clean already has
    trips_clean["*"],
    # add the zone's name, call this new column "pickup_zone"
    zones["Zone"].alias("pickup_zone"),
    # add the zone's borough, call this new column "pickup_borough"
    zones["Borough"].alias("pickup_borough")
)

# print a small sample so we can check the join worked
print("Sample of joined data:")
trips_with_zone.select("PULocationID", "pickup_zone", "pickup_borough", "fare_amount").show(5)

# import the tool to pull just the date out of a full timestamp
from pyspark.sql.functions import to_date, count, avg

#  AGGREGATE 

# add a new column with just the date (no time) from the pickup timestamp
trips_with_date = trips_with_zone.withColumn("pickup_date", to_date(col("tpep_pickup_datetime")))

# group all trips by date and borough, then calculate two numbers per group
daily_summary = trips_with_date.groupBy("pickup_date", "pickup_borough").agg(
    # count how many trips are in each group
    count("*").alias("trip_count"),
    # calculate the average fare for each group
    avg("fare_amount").alias("avg_fare")
)

# print a sample of the summarized result
print("Sample of aggregated result:")
daily_summary.show(10)

#  WRITE

daily_summary.write.mode("overwrite").parquet("output/daily_summary")

print("Done. Output written to output/daily_summary")

input("Press Enter to stop Spark and exit...")

# shut Spark down cleanly when done
spark.stop()