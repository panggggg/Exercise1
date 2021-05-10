import pika


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="exercise", exchange_type="fanout")

print("Name:")
name = input()
print(type(name))

channel.basic_publish(exchange="exercise", routing_key="", body=name)
print("[X] Sent data message")

connection.close()