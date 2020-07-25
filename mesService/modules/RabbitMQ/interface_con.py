# -*- coding: utf-8 -*-
# @createTime    : 2020/3/24 13:56
# @author  : 王江桥
# @fileName: mq_rpc_server.py
# @email: jiangqiao.wang@mabotech.com
import json
import os
import sys
import pika
from mesService.modules.RabbitMQ import logger
from mesService.modules.ERPInterface.erp_to_mes.deviartion.receive_deviating import DeviationOrder
from mesService.modules.ERPInterface.erp_to_mes.bom.reveive_bom import BomOrder
from mesService.modules.ERPInterface.erp_to_mes.item.reveive_item import ItemOrder
from mesService.modules.ERPInterface.erp_to_mes.wip_order.reveive_wiporder import WipOrderInterface
from mesService.modules.ERPInterface.erp_to_mes.wip_sequence.reveive_sequence import SequenceInterface
from mesService.config import PRESENT_WORK_MODE
from mesService.config import CURRENT_ENV, config_dict




func_dict = {
    "DeviationOrder": {"parse_xml": "parse_xml", "insertDatabase": "insertDatabase"},
    "BomOrder": {"parse_xml": "parse_xml", "insertDatabase": "insertDatabase"},
    "ItemOrder": {"parse_xml": "parse_xml", "insertDatabase": "insertDatabase"},
    "WipOrderInterface": {"parse_xml": "analysisFromXML", "insertDatabase": "insertDatabase"},
    "SequenceInterface": {"parse_xml": "analysisFromXML", "insertDatabase": "insertDatabase"},
}


# 回调函数
def callback(data):
    # 实例化类
    # print(data)
    data_str = json.loads(data)
    classname = data_str["classname"]
    xml_data = data_str["xml_data"]
    xml_body = data_str["xml_body"]
    obj = getattr(sys.modules[__name__], classname)(PRESENT_WORK_MODE)
    # data = obj.parse_xml(bytes(xml_data, encoding="utf-8"), xml_body)
    # ret = obj.insertDatabase(data)
    data = getattr(obj, func_dict[classname]["parse_xml"])(bytes(xml_data, encoding="utf-8"), xml_body)
    ret = getattr(obj, func_dict[classname]["insertDatabase"])(data)
    print(ret)

    return ret


# 对RPC请求队列中的请求进行处理
def on_request(ch, method, props, body):
    # print(body, type(body))
    # 调用数据处理方法
    response = callback(body)
    data_str = json.dumps(response)
    print("response",response)
    if "ORA-08177" in str(response):
        ch.basic_reject(method.delivery_tag, True)
        logger.writeLog("重新放入队列:" + str(response), os.path.basename(__file__) + ".log")
    elif "error executing" in str(response):
        ch.basic_reject(method.delivery_tag, True)
        logger.writeLog("重新放入队列:" + str(response), os.path.basename(__file__) + ".log")
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # 将处理结果(响应)发送到回调队列
        ch.basic_publish(exchange='',
                         # reply_to代表回复目标
                         routing_key=props.reply_to,
                         # correlation_id（关联标识）：用来将RPC的响应和请求关联起来。
                         properties=pika.BasicProperties(correlation_id=props.correlation_id,
                                                         delivery_mode=2),
                         body=data_str)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,credentials=credentials))
    # 建立会话
    channel = connection.channel()
    # 声明RPC请求队列
    channel.queue_declare(queue='interfaceRPC', durable=True)

    # 负载均衡，同一时刻发送给该服务器的请求不超过20个
    channel.basic_qos(prefetch_count=20)
    channel.basic_consume(queue='interfaceRPC', on_message_callback=on_request, auto_ack=False)
    print("等待接收rpc请求...")

    # 开始消费
    channel.start_consuming()


if __name__ == '__main__':
    main()
