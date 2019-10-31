# -*- coding: utf-8 -*-
# @createTime    : 2019/10/30
# @author  : 郭辉
# @email: hui.guo@mabotech.com

from xml.etree import ElementTree as ET

class WiptrxInterface:
    # 定义XML中的完工对象
    wiptrxXmlObj = {
        'TransactionID': '',                    # 固定值，接口
        'TransactionType':'',                   #区分具体返回
        'CSN':'',
        'WIPJobNo': '',                         # 工单号
        'WorkOrderStatus':'',                   #订单状态
        'PlantCode': '',                        # 工厂代码
        'ProductionLineNo':'',                 #产线
        'ActualMSBM':'',
        'LastCompletedStation':'',
        'Dummy1':'',
        'Dummy2':'',
        'Dummy3':'',
    }

    # 定义数据库中的完工字段，由WIP_ORDER查询
    wiptrxDatabaseObj = {
        'TransactionID':'WIPTRX',             #固定值
        'wiporderno': '',                     #工单编号
        'productionlineno':'',               #产线
        'releasedfacility': '',              #工厂代码
    }

    # 将Database字段与XML数据对应绑定  数据流向 数据库--->XML
    def bindDatabase2Xml(self, datalist):
        for obj in datalist:
            self.wiptrxXmlObj['TransactionID'] = obj['TransactionID']                    # 固定值
            self.wiptrxXmlObj['WIPJobNo'] = obj['wiporderno']                            # 工单编号
            self.wiptrxXmlObj['productionlineno'] = obj['productionlineno']            # 工单编号
            self.wiptrxXmlObj['PlantCode'] = obj['releasedfacility']                   # 工厂代码
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

        return new