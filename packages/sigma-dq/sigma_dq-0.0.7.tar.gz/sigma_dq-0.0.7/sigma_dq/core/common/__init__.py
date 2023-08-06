from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]") \
    .appName('sigma_dq') \
    .getOrCreate()
