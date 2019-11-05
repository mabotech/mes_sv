# -*- coding: utf-8 -*-
# @createTime    : 2019/10/30
# @author  : 郭辉
# @email: hui.guo@mabotech.com

import json
from flask import current_app
from xml.etree import ElementTree as ET

class WiptrxInterface:
    # 定义XML中的完工对象
    wiptrxXmlObj = {
        'TransactionID': '',                    # 固定值，接口
        'TransactionType':'',                   #区分具体返回
        'CSN':'',                                #半成品序列号
        'WIPJobNo': '',                         # 工单号
        'WorkOrderStatus':'',                   #订单状态
        'PlantCode': '',                        # 工厂代码
        'ProductionLineNo':'',                  #产线
        'ActualMSBM':'',
        'LastCompletedStation':'',              #上一个完工工位
        'Dummy1':'',
        'Dummy2':'',
        'Dummy3':'',
    }

    # 定义数据库中的完工字段，由WIP_ORDER查询
    wiptrxDatabaseObj = {
        'TransactionID':'',             #固定值
        'wiporderno': '',                     #工单编号
        'productionlineno':'',               #产线
        'releasedfacility': '',              #工厂代码
    }

    # 将Database字段与XML数据对应绑定  数据流向 数据库--->XML
    def bindDatabase2Xml(self, datalist):
        for obj in datalist:
            self.wiptrxXmlObj['TransactionID'] = obj['transactionid']                    # 固定值
            self.wiptrxXmlObj['WIPJobNo'] = obj['wiporderno']                            # 工单编号
            self.wiptrxXmlObj['productionlineno'] = obj['productionlineno']            # 工单编号
            self.wiptrxXmlObj['PlantCode'] = obj['releasedfacility']                   # 工厂代码
            self.wiptrxXmlObj['TransactionType'] = obj['transactiontype']
        return self.wiptrxXmlObj

    # 生成上线的XML文件(实时回传)
    def genOnlineXML(self, wiptrxDatalist):

        # 将字段转换为对应的XML字段
        wiptrxXMLlist = self.bindDatabase2Xml(wiptrxDatalist)
        print('转换后:',wiptrxXMLlist)

        # 创建祖节点
        sequenceRoot = ET.Element("root")

        # 在节点树下生成数据节点
        for item in wiptrxXMLlist:
            ET.SubElement(sequenceRoot, item).text = wiptrxXMLlist[item]

        new = ET.tostring(sequenceRoot, encoding='utf-8')

        new_log=str(new, 'utf-8')
        print(new_log)

        sql_wiptrxDatalist=wiptrxDatalist[0]
        print(sql_wiptrxDatalist)
        transactionid=sql_wiptrxDatalist['TransactionID']

        message = { "wiporder": sql_wiptrxDatalist["wiporderno"],
                    "context": new_log}
        json_message = json.dumps(message)
        base_sql = """select update_interface_log('{}');"""
        sql = base_sql.format(json_message)
        print('1',sql)
        current_app.db.query(sql)

        return new