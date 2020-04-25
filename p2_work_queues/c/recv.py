#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   4/16/20 2:33 PM
@Author   :   Fangyang
"""
import time
import pika


def callback(ch, method, props, body):
    print(f"[*] Received {body}")
    time.sleep(body.count(b'.'))
    print(f"[*] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)

channel.basic_qos(prefetch_count=1)  # 保证相同的任务这个worker身上只有一个任务, 不额外分配任务
channel.basic_consume(
    queue="task_queue",
    on_message_callback=callback,
    # auto_ack=True,  # 默认为false, client处理消息时消息不丢失, client die了,由下一个client继续
)

print(f"[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

if __name__ == "__main__":
    pass
