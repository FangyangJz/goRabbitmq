#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   2020/4/5 下午9:48
@Author   :   Fangyang
"""

import asyncio
from aio_pika import connect, Message


async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    # Sending the message
    await channel.default_exchange.publish(
        Message(b'Hello World! from aio-pika'),
        routing_key='hello',
    )

    print(" [x] Sent 'Hello World!'")

    await connection.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))