# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com
import requests
import xmltodict
from lxml import etree
import sys
import json

sys.path.append(r'/home/test01/messervice')

from mesService import config_dict
from mesService.lib.pgwrap.db import connection
from mesService.constants import IAC_HOST


class Iac(object):
    def __init__(self):
        self.db = self.create_conn('development')
        self.url = IAC_HOST

    def format_soa_xml(self, iac_xml):
        soa_format_xml = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" >
   <soap:Body>
<msfm:MSFM_BFCEC_051_SendIACInterfaceService xmlns:msfm="http://www.cummins.com/MSFM_BFCEC_051_SendIACInterface">
    <msfm:DATA><![CDATA[<DATA>
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
			{iac_xml}
		</ROOT>
	</InputParameters>
</IAC_IMPORT_Input>
</DATA>
 ]]></msfm:DATA>
</msfm:MSFM_BFCEC_051_SendIACInterfaceService>
   </soap:Body>
</soap:Envelope>"""
        return soa_format_xml.format(iac_xml=iac_xml)

    def dict_to_xml(self, dict_data):
        root = etree.Element('ROOT_ITEM')
        for k, v in dict_data.items():
            # node = etree.SubElement(root, k.capitalize())
            node = etree.SubElement(root, k.upper())
            if v:
                node.text = str(v)

        tree = etree.ElementTree(root)
        # tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
        xml_str = etree.tostring(tree, encoding='utf-8', pretty_print=True).decode()
        # xml_str = etree.tostring(tree, encoding='utf-8').decode()

        return xml_str

    def get_iac_data(self):

        sql_str = "select get_iac();"
        result = self.db.query(sql_str)
        return result[0]['get_iac']

    def data_to_log(self, data):
        """
        function:iac回冲失败时，插入interfacelog日志
        :return:
        """
        # sql_str = "select job_iac_to_interfacelog('{0}');".format(json.dumps(data))
        # result = self.db.query(sql_str)
        # # return result[0]['job_iac_to_interfacelog']
        # print("result>>", result)
        pass

    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

    def set_to_erp(self, xml):

            reqobj = requests.Session()
            reqobj.auth = ('MSFM', 'MSFM202004210945')
            response = reqobj.post(
                url=self.url,
                data=xml,
                headers={
                    'Content-Type': 'text/xml;charset=UTF-8',
                },
            )

            # 捕获ERP回馈信息
            # s = response.content
            # tree = etree.HTML(s)
            # xml_str1 = etree.tostring(tree)
            # print('xml_str1',xml_str1)
            # list_data = xmltodict.parse(xml_str1)['html']['body']['envelope']['body'][
            #     'getmsfm_bfcec_051_sendiacinterfaceresponse']['message']['outputparameters']['x_return_status']
            # print('list_data', list_data)
            # if list_data == 'S':
            #     print('进来了')
            try:
                message = {'application': 'MES',
                           'transactionid': 'IAC',
                           'transactiontype': 'IAC回冲',
                           'message': 'IAC待回冲',
                           'actionstatus': '插入',
                           'wiporder': '',
                           'result': 0,
                           'context': xml,
                           'createdby': ''
                           }
                print(message)
                json_message = json.dumps(message)
                print(json_message)
                base_sql = """select insert_outflow_log('{}');"""
                sql = base_sql.format(json_message)
                print('S', sql)
                result = self.db.query(sql)

                # return response
            except Exception:
                pass


if __name__ == '__main__':
    iac = Iac()
    dataset = iac.get_iac_data()
    s=[]
    if dataset:
        for data in dataset:
            xml = iac.dict_to_xml(data)
            s.append(xml)
        tempres = "".join(s)
        soa_xml = iac.format_soa_xml(tempres)
        print('soa_xml',soa_xml)
        # response = iac.set_to_erp(soa_xml)
        # 获取状态码
        # request_status = response.status_code
        # print(request_status)
        # request_status = 2002

        # iac回冲错误
        # if request_status != 200:
            # dat = {"productno": data["parentno"], "xml": xml}
            # 写入错误日志信息
            # iac.data_to_log(dat)

    else:
        print("当前无IAC回冲！")
