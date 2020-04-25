#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   4/16/20 4:37 PM
@Author   :   Fangyang
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout',
    durable=True
)

msg = "hello......"
channel.basic_publish(
    exchange="logs",
    routing_key="",
    body=msg,
    # properties=pika.BasicProperties(
    #     delivery_mode=2  # message persistent
    # )
)
print(f"[*] Sent {msg}")
connection.close()
if __name__ == "__main__":
    pass
