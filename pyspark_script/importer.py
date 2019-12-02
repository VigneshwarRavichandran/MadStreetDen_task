from datetime import datetime
import glob
import multiprocessing
import os
import time

from pyspark.sql import SparkSession
import redis

redis_store = redis.StrictRedis(host='redis')
redis_pipe = redis_store.pipeline()

def loading_data(filename):
    spark_sc = SparkSession \
        .builder \
        .appName("Reading large .csv file") \
        .config("spark.some.config.option", "pyspark_config") \
        .getOrCreate()
    datasets = spark_sc.read.csv(filename, header=True, sep=",")
    product_ids = []
    for dataset in datasets.rdd.collect():
        product_id = dataset['id']
        brand = dataset['brand']
        colors = dataset['colors']
        date_added = dataset['dateAdded']
        if all([product_id, brand, colors, date_added]):
            if product_id not in product_ids:
                """
                Storing the datasets values as hash structure
                in the Redis store
                """
                redis_store.hset(product_id, 'id', product_id)
                redis_store.hset(product_id, 'brand', brand)
                redis_store.hset(product_id, 'colors', colors)
                redis_store.hset(product_id, 'date_added', date_added)
                """
                Storing the dateAdded as unixtimestamp 
                datasets values using ordered set structure
                in the Redis store
                """
                timestamp = datetime.strptime(date_added, '%Y-%m-%dT%H:%M:%SZ')
                unix_timestamp = time.mktime(timestamp.timetuple())
                redis_store.zadd('product_timestamp', {product_id: int(unix_timestamp)})
                """
                Storing the Colors datasets as ordered set structure
                in the Redis store
                """
                colors = colors.split(',')
                for color in colors:
                    redis_store.zadd(color.lower(), {product_id: int(unix_timestamp)})
                product_ids.append(product_id)

def import_data_to_redis():
    filenames = glob.glob(os.path.join('./', '*.csv'))
    process = multiprocessing.Pool(len(filenames))
    process.map(loading_data, filenames)
    

if __name__ == '__main__':
    import_data_to_redis()
