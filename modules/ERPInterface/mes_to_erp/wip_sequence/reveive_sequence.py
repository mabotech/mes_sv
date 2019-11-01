# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28
# @author  : 郭辉
# @email: hui.guo@mabotech.com

# import re
# import time
# from lxml import etree
#
# class SequenceInterface:
#     # 定义XML中的排序对象
#     sequenceXmlObj = {
#         'TransactionID': 'SEQDWNLOAD',  # 固定值
#         'Status': 'I',  # I插入U更新N删除
#         'WIPJobNo': '',  # 工单号
#         'SequenceNumber': '',  # 排序序列
#         'PlantCode': '',  # 工厂代码
#         'BatchID': '',      #批次
#     }
#
#     # 定义数据库中的排序对象 Wip_Sequence
#     sequenceDatabaseObj = {
#         'TransactionID':'', # 固定值,区分发送哪个系统
#         'active':'', # I插入U更新N删除
#         'wiporderno': '',  # 工单编号
#         'originalorderindex': '',  # 原始序号
#         'releasedfacility': '',  # 工厂
#         'originalbatchid': ''  # 批次
#     }
#
#     # 将XML数据与Database字段对应绑定  数据流向 XML--->数据库
#     def bindXml2Database(self):
#         self.sequenceDatabaseObj['active'] = self.sequenceXmlObj['Status']  # I插入U更新N删除
#         self.sequenceDatabaseObj['wiporderno'] = self.sequenceXmlObj['WIPJobNo']  # 工单号
#         self.sequenceDatabaseObj['originalorderindex'] = self.sequenceXmlObj['SequenceNumber']  # 序号
#         self.sequenceDatabaseObj['releasedfacility'] = self.sequenceXmlObj['PlantCode']  # 工厂代码
#         self.sequenceDatabaseObj['originalbatchid'] = self.sequenceXmlObj['BatchID']  # 批次号
#

