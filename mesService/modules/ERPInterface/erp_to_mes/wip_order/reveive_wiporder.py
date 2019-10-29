# -*- coding: utf-8 -*-
# @createTime    : 2019/10/26
# @author  : 郭辉
# @email: hui.guo@mabotech.com

import re
import time
from lxml import etree

class WipOrderInterface:
    def __init__(self, path=r'E:\mesService\mesService\modules\ERPInterface\erp_to_mes\wip_order\test_wiporder.xml'):
        self.xml_path = path

    def parse_xml(self):
        """
        function:xml数据解析
        :return: 返回列表数据
        """
        print(self.xml_path)
        tree = etree.parse(self.xml_path)
        xml_str = etree.tostring(tree)
        dict_data = self.analysisFromXML(xml_str)

        return dict_data

    # XML中的订单对象
    wipoderXmlObj = {
        'TransactionID': '',             #固定值，区分发送哪个系统
        'Status': '',                    #A插入/O取消
        'BuildScheduleDate': '',        #工单上线日期
        'CustomerRequestDate': '',      #传输请求日期
        'BuildQuantity': '',             #工单建造数量
        'SONumber':'',                   #物料号
        'StructureDate': '',            #BOM版本日期
        'UnitNumber': '',               #工单号后6位
        'WIPJobNo': '',                 #工单号
        'ProductionLineNo': '',        #生产线
        'CustomerCode':'',             #顾客代码
        'PlantCode': '',               #工厂代码
        'WOType': '',                  #固定值

    }

    #数据库中的订单对象--WIP_ORDER
    wipoderDatabaseObj = {
        'TransactionID': '',             #固定值，区分发送哪个系统
        'active':'',                     #A插入/O取消（工单状态）
        'scheduledstartdate': '',       #工单上线日期
        'releasedate': '',              #传输请求日期
        'orderquantity':'',             #工单建造数量
        'productno': '',                #物料号
        'structuredate': '',           #BOM版本日期
        'UnitNumber': '',              #工单号后6位
        'wiporderno': '',              #工单号
        'productionlineno': '',       #生产线
        'releasedfacility': '',       #工厂代码
        'wipordertype': '',           #固定值

    }

    #将XML数据与Database字段对应绑定
    def bindXml2Database(self):
        self.wipoderDatabaseObj['TransactionID'] = self.wipoderXmlObj['TransactionID']                                     #固定值
        self.wipoderDatabaseObj['active'] = self.xmltype2Inttype(self.wipoderXmlObj['Status'])                              #1新建/18取消（工单状态）
        self.wipoderDatabaseObj['scheduledstartdate'] = self.xmldate2Timestamp(self.wipoderXmlObj['BuildScheduleDate'])   #计划开工时间
        self.wipoderDatabaseObj['orderquantity'] = self.wipoderXmlObj['BuildQuantity']                                      #工单数量
        self.wipoderDatabaseObj['productno'] =  self.wipoderXmlObj['SONumber']                                              #物料号
        self.wipoderDatabaseObj['structuredate'] = self.xmldate2Timestamp(self.wipoderXmlObj['StructureDate'])           #BOM日期
        self.wipoderDatabaseObj['UnitNumber'] = self.wipoderXmlObj['UnitNumber']                                         #工单号后6位
        self.wipoderDatabaseObj['wiporderno'] = self.wipoderXmlObj['WIPJobNo']                                           #工单编号
        self.wipoderDatabaseObj['productionlineno'] = self.wipoderXmlObj['ProductionLineNo']                            #产线
        self.wipoderDatabaseObj['releasedfacility'] = self.wipoderXmlObj['PlantCode']                                   #发布工厂
        self.wipoderDatabaseObj['wipordertype'] =self.xmltype2Inttype( self.wipoderXmlObj['WOType'])                    #固定值

    #将XML日期类型转为时间戳
    def xmldate2Timestamp(self,xmldate):
        xmldate = '20' + xmldate
        print(xmldate)
        xmltimestamp = int(time.mktime(time.strptime(xmldate, '%Y%m%d')))
        restime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(xmltimestamp))
        return restime

    #将订单类型由文字转换为整形
    def xmltype2Inttype(self, orderxmltype):
        wipordertype = 1
        if orderxmltype == 'NORMAL':
            wipordertype = 110
        else:
            wipordertype = 1

        return wipordertype


    #从XML文件中解析数据并将其转换为数据库字段
    def analysisFromXML(self,xmlfile):
        #解析XML
        wiporderxml = etree.parse(xmlfile, etree.XMLParser())
        wiporderDatabaselist = [] #存放解析后的数据库字段类型的数据
        wiporderroot = wiporderxml.getroot()
        for wipjobload in wiporderroot:
            for wodownload in wipjobload:
                #每个Wodownload标识一个订单数据
                for item in wodownload:
                    itemtag = re.sub("\\{.*?}",'',item.tag)
                    print(itemtag)
                    self.wipoderXmlObj[itemtag] = item.text
                self.bindXml2Database()
                wiporderDatabaselist.append(self.wipoderDatabaseObj.copy())
        # logger.writeLog("解析工单XML成功---->" + xmlfile)
        return wiporderDatabaselist