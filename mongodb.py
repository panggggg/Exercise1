import pymongo
import pika

client = pymongo.MongoClient("localhost", 27017)

mydb = client["mydb"]

mycol = mydb["people"]

data = {"name": "Pang", "age": 21}
mycol.insert_one(data)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("test")
queue_name = queue.method.queue

channel.queue_bind(queue=queue_name, exchange="exercise", routing_key="")


def callback(ch, method, properties, body):

    print("[X] Get data")
    print(body)
    print("[X] Done")

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waitting for data")

channel.start_consuming()