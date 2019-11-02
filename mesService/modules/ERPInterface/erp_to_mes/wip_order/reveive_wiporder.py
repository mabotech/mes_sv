# -*- coding: utf-8 -*-
# @createTime    : 2019/10/26
# @author  : 郭辉
# @email: hui.guo@mabotech.com

import re
import time
import xmltodict
from lxml import etree
from flask import request

class WipOrderInterface:

    # XML中的订单对象啊
    wipoderXmlObj = {
        'transactionid': '',             #固定值，区分发送哪个系统
        'status': '',                    #A插入/O取消
        'buildscheduledate': '',        #工单上线日期
        'customerrequestdate': '',      #传输请求日期
        'buildquantity': '',             #工单建造数量
        'sonumber':'',                   #物料号
        'structuredate': '',            #BOM版本日期
        'unitnumber': '',               #工单号后6位
        'wipjobno': '',                 #工单号
        'productionlineno': '',        #生产线
        'customercode':'',             #顾客代码
        'plantcode': '',               #工厂代码
        'wotype': '',                  #固定值
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
        self.wipoderDatabaseObj['TransactionID'] = self.wipoderXmlObj['transactionid']                                     #固定值
        self.wipoderDatabaseObj['active'] = self.xmltype2Inttype(self.wipoderXmlObj['status'])                              #1新建/18取消（工单状态）
        self.wipoderDatabaseObj['scheduledstartdate'] = self.xmldate2Timestamp(self.wipoderXmlObj['buildscheduledate'])  #计划开工时间
        self.wipoderDatabaseObj['orderquantity'] = self.wipoderXmlObj['buildquantity']                                      #工单数量
        self.wipoderDatabaseObj['productno'] =  self.wipoderXmlObj['sonumber']                                              #物料号
        self.wipoderDatabaseObj['structuredate'] = self.xmldate2Timestamp(self.wipoderXmlObj['structuredate'])         #BOM日期
        self.wipoderDatabaseObj['UnitNumber'] = self.wipoderXmlObj['unitnumber']                                         #工单号后6位
        self.wipoderDatabaseObj['wiporderno'] = self.wipoderXmlObj['wipjobno']                                           #工单编号
        self.wipoderDatabaseObj['productionlineno'] = self.wipoderXmlObj['productionlineno']                            #产线
        self.wipoderDatabaseObj['releasedfacility'] = self.wipoderXmlObj['plantcode']                                   #发布工厂
        self.wipoderDatabaseObj['wipordertype'] =self.xmltype2Inttype( self.wipoderXmlObj['wotype'])                    #固定值
        self.wipoderDatabaseObj['progressstatus'] = 110                                                                 #工单状态默认待排产
    #将XML日期类型转为时间戳
    def xmldate2Timestamp(self,xmldate):
        print(xmldate)
        xmldate = '20' + xmldate
        print(xmldate)
        xmltimestamp = int(time.mktime(time.strptime(xmldate, '%Y%m%d')))
        restime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(xmltimestamp))
        return restime

    #将订单类型由文字转换为整形
    def xmltype2Inttype(self, orderxmltype):
        wipordertype = 1
        if orderxmltype == 'NORMAL':
            wipordertype = 1
        elif orderxmltype == 'O':
            wipordertype = 2

        return wipordertype


    #从XML文件中解析数据并将其转换为数据库字段
    def analysisFromXML(self):
        #解析XML
        xml_str = request.data
        tree = etree.HTML(xml_str)
        xml_str = etree.tostring(tree)
        list_data = xmltodict.parse(xml_str)['html']['body']['wipjobload']['wodownload']
        print(list_data)
        wiporderDatabaselist=[]
        for key,val in list_data.items():
            print(key,val)
            self.wipoderXmlObj[key] = val
        self.bindXml2Database()
        wiporderDatabaselist.append(self.wipoderDatabaseObj.copy())
        print(wiporderDatabaselist)
        return wiporderDatabaselist