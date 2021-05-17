from logging import info
from weakref import ProxyTypes
import pika
from pymongo import mongo_client
from pymongo import collection
import redis
import json

from database.mongodb import MongoDB
from config.development import config

mongo_config = config["mongo_config"]
print("Mongo_config", mongo_config)

mongo_db = MongoDB(
    mongo_config["host"],
    mongo_config["port"],
    mongo_config["user"],
    mongo_config["password"],
    mongo_config["auth_db"],
    mongo_config["db"],
    mongo_config["collection"],
)
mongo_db._connect()


# client = pymongo.MongoClient("localhost", 27018)

# mydb = client["mydb"]

# mycol = mydb["people"]


redis_connection = redis.Redis(host="localhost", port=6380, db=0)  # connect redis
# db 0-15


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", port=5673))
channel = connection.channel()
print(channel)

queue = channel.queue_declare("test")
queue_name = queue.method.queue

channel.queue_bind(queue=queue_name, exchange="exercise", routing_key="exercise")


def callback(ch, method, properties, body):

    payload = json.loads(body)
    # data = body.decode("UTF-8")

    print("[X] Get data")

    print(
        f"""
        Username: {payload.get('username')}
        Email: {payload.get('email')}
        
        """
    )

    name = payload.get("username")

    if redis_connection.get(name) is None:  # get Key ถ้ายังไม่มี Key นี้
        db = payload
        mongo_db.insert(db)  # save ลง db
        redis_connection.set(name, name)  # set Key Value
        print("Save name into the MongoDB")

    else:  # มี Key นี้แล้ว
        print("This name already has in the MongoDB")

    print("[X] Done")

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waitting for data")

channel.start_consuming()