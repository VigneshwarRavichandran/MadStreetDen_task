from collections import Counter
from datetime import datetime
import time

from flask import request, Flask, jsonify
import redis
from utilities import convert

app = Flask(__name__)
redis_store = redis.StrictRedis(host='redis')
redis_pipe = redis_store.pipeline()


@app.route('/getRecentItem', methods=['GET'])
def get_recent_item():
    date = request.args.get('date')
    if date is None:
        return jsonify({
            'message': 'Invalid parameters'
        }), 422
    try:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({
            'message': 'Invalid Date format'
        }), 422
    start_datetime = datetime.combine(datetime_obj, datetime.min.time())
    end_datetime = datetime.combine(datetime_obj, datetime.max.time())
    unix_start_timestamp = time.mktime(start_datetime.timetuple())
    unix_end_timestamp = time.mktime(end_datetime.timetuple())
    """
    Getting items from ordered dataset 'product_timestamp'
    A tuple which contains the product ids which are added 
    in the given date is obtained using zrangebyscore
    Accessing the first value gives the most recent item
    """
    recent_item = redis_store.zrangebyscore(
        'product_timestamp', int(unix_start_timestamp), int(unix_end_timestamp), withscores=True)[0]
    recent_itemid = recent_item[0]
    product = convert(redis_store.hgetall(recent_itemid))
    return jsonify(product)


@app.route('/getBrandsCount', methods=['GET'])
def get_brands_count():
    date = request.args.get('date')
    if date is None:
        return jsonify({
            'message': 'Invalid parameters'
        }), 422
    try:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({
            'message': 'Invalid Date format'
        }), 422
    start_datetime = datetime.combine(datetime_obj, datetime.min.time())
    end_datetime = datetime.combine(datetime_obj, datetime.max.time())
    unix_start_timestamp = time.mktime(start_datetime.timetuple())
    unix_end_timestamp = time.mktime(end_datetime.timetuple())
    """
    Getting items from ordered dataset 'product_timestamp'
    A tuple which contains the product ids which are added 
    in the given date is obtained using zrangebyscore
    Getting the brands of the products and 
    using Counter to get the brand count on the given date
    """
    item_ids = redis_store.zrangebyscore(
        'product_timestamp', int(unix_start_timestamp), int(unix_end_timestamp), withscores=False)
    for item_id in item_ids:
        redis_pipe.hget(item_id, 'brand')
    brands = convert(redis_pipe.execute())
    return jsonify({
        'result': Counter(brands).most_common()
    })


@app.route('/getItemsbyColor', methods=['GET'])
def get_items_by_color():
    try:
        product_color = request.args.get('color').lower()
    except AttributeError:
        return jsonify({'message': 'Invalid parameters'}), 422
    """
    Getting items from ordered dataset 'product_color'
    zrevrange gives the range of recently added products in
    the given color
    """
    item_ids = redis_store.zrevrange(
        product_color, 0, 9)
    for item_id in item_ids:
        redis_pipe.hgetall(item_id)
    products = convert(redis_pipe.execute())
    return jsonify({
        'result': products
    })


if __name__ == '__main__':
    while(True):
        try:
            if(redis_store.ping()):
                app.run()
        except redis.exceptions.ConnectionError:
            print("Please make sure to connect with Redis. Restarting in 30 seconds")
            time.sleep(5)
