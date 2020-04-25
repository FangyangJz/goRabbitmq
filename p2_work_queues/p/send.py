#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   4/16/20 2:41 PM
@Author   :   Fangyang
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(
    queue="task_queue",
    durable=True  # 队列持久化, 在RabbitMQ启动时还在
)

msg = "hello......"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=msg,
    properties=pika.BasicProperties(
        delivery_mode=2  # message persistent
    )
)
print(f"[*] Sent {msg}")
connection.close()

if __name__ == "__main__":
    pass
