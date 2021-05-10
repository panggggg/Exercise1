import pymongo
import pika
import redis

client = pymongo.MongoClient("localhost", 27017)

mydb = client["mydb"]

mycol = mydb["people"]
# print(client.list_database_names())

redis_connection = redis.Redis(host="localhost", port=6379, db=0)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("test")
queue_name = queue.method.queue

channel.queue_bind(queue=queue_name, exchange="exercise", routing_key="")


def callback(ch, method, properties, body):

    data = body.decode("UTF-8")

    print("[X] Get data")
    print(type(data))
    print(
        f"""
        Name: {data}
        """
    )

    if redis_connection.get(data) is None:
        db = {"name": data}
        mycol.insert_one(db)
        redis_connection.set(data, data)
        print("Save name to MongoDB")
    else:
        print("Found Name in MongoDB")

    print("[X] Done")

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waitting for data")

channel.start_consuming()