# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28
# @author  : 郭辉
# @email: hui.guo@mabotech.com

import re
from lxml import etree

class SequenceInterface:
    # 定义XML中的排序对象
    sequenceXmlObj = {
        'TransactionID': 'SEQDWNLOAD',              #固定值
        'Status': 'I',                               #I插入U更新N删除
        'WIPJobNo': '',                              #工单号
        'SequenceNumber': '',                       #排序序列
        'PlantCode': '',                            #工厂代码
        'BatchID': '',                              #批次
    }

    # 定义数据库中的排序对象 Wip_Sequence
    sequenceDatabaseObj = {
        'TransactionID':'',                   #固定值,区分发送哪个系统
        'status':'',                          #I插入U更新N删除
        'wiporderno': '',                    #工单编号
        'externalIndex': '',                   #原始序号
        'batchid': '',                       #批次
        'facility':''                        #工厂代码
    }

    # 将XML数据与Database字段对应绑定  数据流向 XML--->数据库
    def bindXml2Database(self):
        self.sequenceDatabaseObj['status'] = self.sequenceXmlObj['Status']                             #I插入U更新N删除
        self.sequenceDatabaseObj['wiporderno'] = self.sequenceXmlObj['WIPJobNo']                      #工单号
        self.sequenceDatabaseObj['externalIndex'] = self.sequenceXmlObj['SequenceNumber']               #序号
        self.sequenceDatabaseObj['facility'] = self.sequenceXmlObj['PlantCode']                      #工厂代码
        self.sequenceDatabaseObj['batchid'] = self.sequenceXmlObj['BatchID']                         #批次号

    # 从XML文件中解析数据并将其转换为数据库字段
    def analysisFromXML(self, xmlfile):
        # 解析XML
        sequencexml = etree.parse(xmlfile, etree.XMLParser())
        sequenceDatabaselist = []  # 存放解析后的数据库字段类型的数据
        sequenceroot = sequencexml.getroot()
        for seqdownload in sequenceroot:
            # 每个seqdownload标识一个订单数据
            for item in seqdownload:
                itemtag = re.sub("\\{.*?}", '', item.tag)  # 使用正则表达式去掉多余XML命名空间
                self.sequenceXmlObj[itemtag] = item.text
            self.bindXml2Database()
            sequenceDatabaselist.append(self.sequenceDatabaseObj.copy())
        # logger.writeLog("解析排序XML:成功---->" + xmlfile)
        return sequenceDatabaselist