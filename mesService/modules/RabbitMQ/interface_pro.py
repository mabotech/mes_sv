# -*- coding: utf-8 -*-
# @createTime    : 2020/3/24 13:56
# @author  : 王江桥
# @fileName: mq_rpc_server.py
# @email: jiangqiao.wang@mabotech.com
import json

import pika
import uuid
import os
from mesService.modules.RabbitMQ import logger
from mesService.config import RABBITMQ_HOST


class InterfaceRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,credentials=credentials))
        self.channel = self.connection.channel()

        # durable = True队列持久化
        result = self.channel.queue_declare(queue='', exclusive=True, durable=True)
        self.callback_queue = result.method.queue
        # 客户端订阅回调队列，当回调队列中有响应时，调用`on_response`方法对响应进行处理;
        self.channel.basic_consume(on_message_callback=self.on_response,
                                   queue=self.callback_queue, auto_ack=False)

    # 对回调队列中的响应进行处理的函数
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(method.delivery_tag)

    # 发出RPC请求
    def call(self, classname):
        # 初始化 response
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.tx_select()
        try:
            self.channel.basic_publish(exchange='',
                                       routing_key='interfaceRPC',
                                       properties=pika.BasicProperties(
                                           reply_to=self.callback_queue,
                                           correlation_id=self.corr_id,
                                           content_type="text/plain"
                                       ),
                                       body=classname)
            self.channel.tx_commit()
        except:
            self.channel.tx_rollback()
            raise Exception("message to queue fail")

        while self.response is None:
            self.connection.process_data_events()

        data_str = json.loads(self.response)
        return data_str


if __name__ == '__main__':
    fibonacci_rpc = InterfaceRpcClient()
    response = fibonacci_rpc.call(json.dumps('abc'))
    print("得到远程结果响应%r" % response)
