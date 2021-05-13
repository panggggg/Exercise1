import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", port=5673))
channel = connection.channel()

channel.exchange_declare(exchange="exercise", exchange_type="fanout")

info = {}


print("Username:")
username = input()
info["username"] = username

print("Email:")
email = input()
info["email"] = email

print(info)

channel.basic_publish(exchange="exercise", routing_key="", body=json.dumps(info))
print("[X] Sent data message")

connection.close()