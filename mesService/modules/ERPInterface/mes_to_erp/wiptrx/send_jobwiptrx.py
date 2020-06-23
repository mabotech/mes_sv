import requests
from flask import current_app, request, jsonify
from lxml import etree
import sys
import json

from xlrd.xlsx import ET

sys.path.append(r'/home/test01/messervice')

from mesService import config_dict
from mesService.lib.pgwrap.db import connection
from mesService.constants import ERP_HOST


class WiptrxInterface(object):
    def __init__(self):
        self.db = self.create_conn('development')
        self.url = ERP_HOST

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
            self.wiptrxXmlObj['WORKORDERSTATUS'] = ' '
            self.wiptrxXmlObj['PRODUCTIONLINENO'] = obj['productionlineno']            #产线
            self.wiptrxXmlObj['LASTCOMPLETEDSTATION'] = obj['currentworkcenter']        #最后完成工位
            self.wiptrxXmlObj['ACTUALMSBM'] = ' '

            if not obj['currentworkcenter']:
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


    def get_wiptrx_data(self):

        json_data=str({"wiporderno":"SO12555000125","releasedfacility":"ISG","transactiontype":"ENGSCRAP"})
        # json_data = str(request.data, 'utf-8')

        # 创建sql语句
        base_sql = """select plv8_get_wiptrx('{}');"""

        # 执行sql语句
        sql = base_sql.format(json_data)
        print("执行sql语句", sql)
        result = current_app.db.query(sql)

        dalist = []
        sql_result = result[0].get('plv8_get_wiptrx')
        print("返回结果：", sql_result)

        if 'error' in sql_result:
            return jsonify(sql_result)
        for item in sql_result:
            offlineobj = self.wiptrxDatabaseObj
            offlineobj['wiporderno'] = item['wiporderno']  # 工单编号
            offlineobj['releasedfacility'] = item['releasedfacility']  # 工厂代码
            offlineobj['productionlineno'] = item['productionlineno']  # 产线
            offlineobj['transactiontype'] = item['transactiontype']
            offlineobj['transactionid'] = item['transactionid']
            offlineobj['serialno'] = item['serialno']
            offlineobj['currentworkcenter'] = item['currentworkcenter']

            dalist.append(offlineobj.copy())

        return dalist

    def data_to_log(self, data,xml):
        """
        发送后更新接口日志
        :return:
        """
        sql_wiptrxDatalist = data[0]
        message = {"wiporder": sql_wiptrxDatalist["wiporderno"],
                   "context": xml}
        json_message = json.dumps(message)
        base_sql = """select update_interface_log('{}');"""
        sql = base_sql.format(json_message)

        current_app.db.query(sql)


    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

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

        return new_xml


    def set_to_erp(self,data, xml):
        try:
            reqobj = requests.Session()
            reqobj.auth = ('MSFM', 'MSFM202004210945')
            response = reqobj.post(
                url=self.url,
                data=xml,
                headers={
                    'Content-Type': 'application/xml',
                },
            )

            self.data_to_log(data, xml)
            return response

        except Exception:
            pass


if __name__ == '__main__':
    wiptrx = WiptrxInterface()
    dataset = wiptrx.get_wiptrx_data()
    if dataset:
        for data in dataset:
            xml = wiptrx.genOnlineXML(data)
            response = wiptrx.set_to_erp(data,xml)

            # 获取状态码
            request_status = response.status_code
            print(request_status)
            # request_status = 2002


            if request_status == 200:
                pass


    else:
        print("当前无回冲类信息！")
