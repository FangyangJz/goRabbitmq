#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   2020/4/5 下午9:38
@Author   :   Fangyang
"""

import pika


def callback(ch, method, props, body):
    print(f"[*] Received {body}")


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_consume(
    queue="hello",
    on_message_callback=callback,
    auto_ack=True,
)

print(f"[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

if __name__ == "__main__":
    pass
