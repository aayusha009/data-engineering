#running pyspark locally on the machine 

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("week_09").master("local[*]")\
    .getOrCreate()

print ("spark is running locally on the machine")

spark.stop()

