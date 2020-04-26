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
        'CSN':' ',                                #半成品序列号
        'WIPJobNo': '',                         # 工单号
        'WorkOrderStatus':'',                   #订单状态
        'PlantCode': '',                        # 工厂代码
        'ProductionLineNo':'',                  #产线
        'ActualMSBM':'',
        'LastCompletedStation':' ',              #上一个完工工位
        'Dummy1':'',
        'Dummy2':'',
        'Dummy3':'',
    }

    # 定义数据库中的完工字段，由WIP_ORDER查询
    wiptrxDatabaseObj = {
        'TransactionID':'',                    #固定值
        'wiporderno': '',                     #工单编号
        'productionlineno':'',               #产线
        'releasedfacility': '',              #工厂代码
    }

    # 将Database字段与XML数据对应绑定  数据流向 数据库--->XML
    def bindDatabase2Xml(self, datalist):
        for obj in datalist:
            self.wiptrxXmlObj['TransactionID'] = obj['transactionid']                    # 固定值
            self.wiptrxXmlObj['TransactionType'] = obj['transactiontype']
            self.wiptrxXmlObj['CSN'] = obj['serialno']                                    #二维码
            self.wiptrxXmlObj['WIPJobNo'] = obj['wiporderno']                            # 工单编号
            self.wiptrxXmlObj['WorkOrderStatus'] = ' '
            self.wiptrxXmlObj['PlantCode'] = obj['releasedfacility']                    # 工厂代码
            self.wiptrxXmlObj['ProductionLineNo'] = obj['productionlineno']            #产线
            self.wiptrxXmlObj['ActualMSBM'] = ' '
            self.wiptrxXmlObj['LastCompletedStation'] = obj['currentworkcenter']        #最后完成工位
            if not obj['currentworkcenter']:
                self.wiptrxXmlObj['LastCompletedStation'] = ' '
            if not obj['serialno']:
                self.wiptrxXmlObj['CSN'] = ' '
            self.wiptrxXmlObj['Dummy1'] = ' '
            self.wiptrxXmlObj['Dummy2'] = ' '
            self.wiptrxXmlObj['Dummy3'] = ' '

        return self.wiptrxXmlObj

    def format_soa_xml(self, new):
        soa_format_xml = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" >
   <soap:Body>
<msfm:MSFM_BFCEC_052_SendMachiningOrderTransService xmlns:msfm="http://www.cummins.com/MSFM_BFCEC_052_SendMachiningOrderTrans">
    <msfm:DATA>![CDATA[<DATA>
<IAC_IMPORT_Input xmlns="http://xmlns.oracle.com/apps/xxc/rest/SYNCIAC/iac_import/">
	<RESTHeader xmlns="http://xmlns.oracle.com/apps/xxc/rest/SYNCIAC/header">
		<Responsibility></Responsibility>
		<RespApplication></RespApplication>
		<SecurityGroup></SecurityGroup>
		<NLSLanguage>SIMPLIFIED CHINESE</NLSLanguage>
		<Org_Id>0</Org_Id>
	</RESTHeader>
	<InputParameters>
		<HEAD>
			<BIZTRANSACTIONID>ERP_SYC_001_2020041715031100</BIZTRANSACTIONID>
			<COUNT>1</COUNT>
			<CONSUMER>ERP</CONSUMER>
			<SRVLEVEL>1</SRVLEVEL>
			<ACCOUNT>SAP</ACCOUNT>
			<PASSWORD>SAP1509030</PASSWORD>
		</HEAD>
		<ROOT>
           {new_xml}
		</ROOT>
	</InputParameters>
</IAC_IMPORT_Input>
</DATA>
 ]]></msfm:DATA>
</msfm:MSFM_BFCEC_052_SendMachiningOrderTransService>
   </soap:Body>
</soap:Envelope>"""

        return soa_format_xml.format(new_xml=new)

    # 生成上线的XML文件(实时回传)
    def genOnlineXML(self, wiptrxDatalist):

        # 将字段转换为对应的XML字段
        wiptrxXMLlist = self.bindDatabase2Xml(wiptrxDatalist)
        print('转换后:',wiptrxXMLlist)

        # 创建祖节点
        sequenceRoot = ET.Element("ROOT_ITEM")

        # 在节点树下生成数据节点
        for item in wiptrxXMLlist:
            ET.SubElement(sequenceRoot, item).text = wiptrxXMLlist[item]

        new = ET.tostring(sequenceRoot, encoding='utf-8')

        new_log=str(new, 'utf-8')
        new_xml = self.format_soa_xml(new_log)
        print("new_xml", new_xml)

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

        return new_xml


