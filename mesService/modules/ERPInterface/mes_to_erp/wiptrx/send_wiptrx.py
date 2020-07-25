# -*- coding: utf-8 -*-
# @createTime    : 2019/10/30
# @author  : 郭辉
# @email: hui.guo@mabotech.com

import json
from flask import current_app
from xml.etree import ElementTree as ET

class WiptrxInterface:
    # 定义XML中的完工对象
    wiptrxXmlObj = { }
    # 定义数据库中的完工字段，由WIP_ORDER查询
    wiptrxDatabaseObj = {
        'TransactionID':'',                    #固定值
        'wiporderno': '',                     #工单编号
        'productionlineno':'',               #产线
        'releasedfacility': '',              #工厂代码
    }

    # 将Database字段与XML数据对应绑定  数据流向 数据库--->XML
    def bindDatabase2Xml(self, datalist):

        print('datalist',datalist)
        for obj in datalist:
            self.wiptrxXmlObj['PLANTCODE'] = obj['releasedfacility']                      # 工厂代码
            self.wiptrxXmlObj['TRANSACTIONID'] = obj['transactionid']                    # 固定值
            self.wiptrxXmlObj['TRANSACTIONTYPE'] = obj['transactiontype']
            self.wiptrxXmlObj['CSN'] = obj['serialno']                                    #二维码
            self.wiptrxXmlObj['WIPJOBNO'] = obj['wiporderno']                            # 工单编号
            self.wiptrxXmlObj['WORKORDERSTATUS'] = obj['workorderstatus']
            self.wiptrxXmlObj['PRODUCTIONLINENO'] = obj['productionlineno']            #产线
            self.wiptrxXmlObj['LASTCOMPLETEDSTATION'] = obj['workcenter']        #最后完成工位
            self.wiptrxXmlObj['ACTUALMSBM'] = ' '

            if not obj['workcenter']:
                self.wiptrxXmlObj['LASTCOMPLETEDSTATION'] = ' '
            if not obj['serialno']:
                self.wiptrxXmlObj['CSN'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE1'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE2'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE3'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE4'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE5'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE6'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE7'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE8'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE9'] = ' '
            self.wiptrxXmlObj['ATTRIBUTE10'] = ' '

        return self.wiptrxXmlObj

    def format_soa_xml(self, new):
        soa_format_xml = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" >
   <soap:Body>
<msfm:MSFM_BFCEC_052_SendMachiningOrderTransService xmlns:msfm="http://www.cummins.com/MSFM_BFCEC_052_SendMachiningOrderTrans">
    <msfm:DATA><![CDATA[<DATA>
<SYNC_TXN_Input xmlns="http://xmlns.oracle.com/apps/xxc/rest/XXCWIPTxnImpSrv/SYNC_WIP_TXN/">
<RESTHeader xmlns="http://xmlns.oracle.com/apps/xxc/rest/XXCWIPTxnImpSrv/header">
<Responsibility></Responsibility>
<RespApplication></RespApplication>
<SecurityGroup></SecurityGroup>
<NLSLanguage>SIMPLIFIED CHINESE</NLSLanguage>
<Org_Id>0</Org_Id>
</RESTHeader>
<InputParameters>
<HEAD>
<BIZTRANSACTIONID>MES_SYC_052_2017061010031100</BIZTRANSACTIONID>
<COUNT>1</COUNT>
<CONSUMER>MES</CONSUMER>
<SRVLEVEL>1</SRVLEVEL>
<ACCOUNT></ACCOUNT>
<PASSWORD></PASSWORD>
</HEAD>
<ROOT>
   {new_xml}
</ROOT>
</InputParameters>
</SYNC_TXN_Input>
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

        print('wiptrxXMLlist',wiptrxXMLlist)
        # 创建祖节点
        sequenceRoot = ET.Element("ROOT_ITEM")

        # 在节点树下生成数据节点
        for item in wiptrxXMLlist:
            ET.SubElement(sequenceRoot, item).text = wiptrxXMLlist[item]

        new = ET.tostring(sequenceRoot, encoding='utf-8')

        new_log=str(new, 'utf-8')
        new_xml = self.format_soa_xml(new_log)


        # sql_wiptrxDatalist=wiptrxDatalist[0]
        # message = { "wiporder": sql_wiptrxDatalist["wiporderno"],
        #             "context": new_xml}
        # json_message = json.dumps(message)
        # base_sql = """select update_interface_log('{}');"""
        # sql = base_sql.format(json_message)

        # current_app.db.query(sql)

        return new_xml,wiptrxXMLlist


