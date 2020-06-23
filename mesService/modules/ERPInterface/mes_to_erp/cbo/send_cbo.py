# -*- coding: utf-8 -*-
# @createTime    : 2019/10/31 14:05
# @author  : 王江桥
# @fileName: send_cbo.py
# @email: jiangqiao.wang@mabotech.com

import json
from flask import current_app
from xml.etree import ElementTree as ET

class CboToXml(object):
    # 定义XML中的完工对象
    cboXmlObj = {}

    # 将Database字段与XML数据对应绑定  数据流向 数据库--->XML
    def bindDatabase2Xml(self, datalist):

        self.cboXmlObj['TRANSACTIONID'] = str(datalist['transactionid'])                   # id值
        self.cboXmlObj['WIPJOBNO'] =  str(datalist['wipjobno'])                       # 工单编号
        self.cboXmlObj['SEQUENCENUMBER'] =  str(datalist['sequencenumber'])                # 排序号
        self.cboXmlObj['PLANTCODE'] =  str(datalist['plantcode'])                           # 工厂
        self.cboXmlObj['PRODUCTIONLINENO'] =  str(datalist['productionlineno'])             # 工厂
        self.cboXmlObj['BATCHID'] =  str(datalist['BATCHID'])                                 # 批次号

        self.cboXmlObj['DUMMY1'] = ' '
        self.cboXmlObj['DUMMY2'] = ' '
        self.cboXmlObj['DUMMY3'] = ' '
        self.cboXmlObj['DUMMY4'] = ' '
        self.cboXmlObj['DUMMY5'] = ' '
        self.cboXmlObj['DUMMY6'] = ' '
        self.cboXmlObj['DUMMY7'] = ' '
        self.cboXmlObj['DUMMY8'] = ' '
        self.cboXmlObj['DUMMY9'] = ' '
        self.cboXmlObj['DUMMY10'] = ' '

        return self.cboXmlObj

    def format_soa_xml(self, new):
        soa_format_xml = """<?xml version="1.0" encoding="UTF-8" ?>
<WO_SORT_IMPORT_Input xmlns="http://xmlns.oracle.com/apps/xxc/rest/WOSORTBACK/wo_sort_import/">
    <RESTHeader xmlns="http://xmlns.oracle.com/apps/xxc/rest/WOSORTBACK/header">
        <Responsibility></Responsibility>
        <RespApplication></RespApplication>
        <SecurityGroup></SecurityGroup>
        <NLSLanguage>SIMPLIFIED CHINESE</NLSLanguage>
        <Org_Id>0</Org_Id>
    </RESTHeader>
    <InputParameters>
        <HEAD>
            <BIZTRANSACTIONID>234</BIZTRANSACTIONID>
            <COUNT></COUNT>
            <CONSUMER></CONSUMER>
            <SRVLEVEL></SRVLEVEL>
            <ACCOUNT></ACCOUNT>
            <PASSWORD></PASSWORD>
        </HEAD>
        <ROOT>
            {new_xml}
        </ROOT>
    </InputParameters>
</WO_SORT_IMPORT_Input>"""

        return soa_format_xml.format(new_xml=new)

    # 生成上线的XML文件(实时回传)
    def genOnlineXML(self, cboDatalist):

        # 将字段转换为对应的XML字段
        # cboXmllist = self.bindDatabase2Xml(cboDatalist)

        # print('cboXmllist', cboXmllist)
        # 创建祖节点
        sequenceRoot = ET.Element("ROOT_ITEM")

        # 在节点树下生成数据节点
        for item in cboDatalist:
            ET.SubElement(sequenceRoot, item).text = cboDatalist[item]

        new = ET.tostring(sequenceRoot, encoding='utf-8')

        new_log = str(new, 'utf-8')


        # sql_wiptrxDatalist = wiptrxDatalist[0]
        # message = {"wiporder": sql_wiptrxDatalist["wiporderno"],
        #            "context": new_xml}
        # json_message = json.dumps(message)
        # base_sql = """select update_interface_log('{}');"""
        # sql = base_sql.format(json_message)

        # current_app.db.query(sql)

        return new_log
