#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   4/16/20 10:49 PM
@Author   :   Fangyang
"""
import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct',
    durable=True,  # golang 那边设置了这个参数, 如果不设置为True, 生成的exchange是同名, 但是是不一致的, py和go先后执行会报错
)

# 让rabbitmq自动生成queue
# channel.queue_declare(
#     queue="task_queue",
#     durable=True  # 队列持久化, 在RabbitMQ启动时还在
# )

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
msg = ' '.join(sys.argv[2:]) or "hello......"
channel.basic_publish(
    exchange="direct_logs",
    routing_key=severity,
    body=msg,
    # properties=pika.BasicProperties(
    #     delivery_mode=2  # message persistent
    # )
)
print(f"[*] Sent {msg}")
connection.close()


if __name__ == "__main__":
    pass
