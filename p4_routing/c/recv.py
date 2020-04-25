#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   4/16/20 10:49 PM
@Author   :   Fangyang
"""
import sys
import time
import pika

###################################
# python recv.py warning > warning.log
# 可以存成一个log文件, 此时控制台没有打印信息
###############################

def callback(ch, method, props, body):
    print(f"[*] routing_key({method.routing_key}) Received {body}")
    # time.sleep(body.count(b'.'))
    # print(f"[*] Done")
    # ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct',
    durable=True,  # golang 那边设置了这个参数, 如果不设置为True, 生成的exchange是同名, 但是是不一致的, py和go先后执行会报错
)

result = channel.queue_declare(
    queue="",  # 不指定queue的名字, 让RBMQ自动生成
    # durable=True,
    exclusive=True,  # 用后即焚, conn关闭,队列删除
)
severities = sys.argv[1:]
if not severities:
    sys.stderr.write(f"Usage : {sys.argv[0]} [info] [warning] [error]\n")
    sys.exit(1)

for severity in severities:
    queue_name = result.method.queue
    channel.queue_bind(
        exchange="direct_logs",
        routing_key=severity,
        queue=queue_name
    )  # 根据queue_name去绑定一个exchange

print(f"[*] Waiting for logs, queue_name: {queue_name}. To exit press CTRL+C")

# channel.basic_qos(prefetch_count=1)  # 保证相同的任务这个worker身上只有一个任务, 不额外分配任务
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    # 默认为false, 需要在callback中定义basic_ack, 如果不人工设置ack, client带着消息die了, produce不会重发
    # 设置成true, 省去人工设置ack, client 带着消息 die 了, produce会重发
    auto_ack=True,
)

# print(f"[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()


if __name__ == "__main__":
    pass
