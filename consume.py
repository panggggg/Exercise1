import pymongo
import pika
import redis

client = pymongo.MongoClient("localhost", 27018)

mydb = client["mydb"]

mycol = mydb["people"]
# print(client.list_database_names())

redis_connection = redis.Redis(host="localhost", port=6380, db=0)  # connect redis
# db 0-15


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

    if redis_connection.get(data) is None:  # get Key ถ้ายังไม่มี Key นี้
        db = {"name": data}
        mycol.insert_one(db)  # save ลง db
        redis_connection.set(data, data)  # set Key Value
        print("Save name into the MongoDB")

    else:  # มี Key นี้แล้ว
        print("This name already has in the MongoDB")

    print("[X] Done")

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waitting for data")

channel.start_consuming()