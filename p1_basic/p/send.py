#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   2020/4/5 下午9:14
@Author   :   Fangyang
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")

msg="hello world from py pika"
channel.basic_publish(
    exchange="",
    routing_key="hello",
    body=msg
)
print(f"[*] Sent {msg}")
connection.close()


if __name__ == "__main__":
    pass
