#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='devo')

channel.basic_publish(exchange='', routing_key='devo', body='Devo Test!')
print(" [x] Sent 'Devo Test!'")
connection.close()