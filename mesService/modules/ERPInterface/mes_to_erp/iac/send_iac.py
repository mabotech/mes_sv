# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com
import requests
from lxml import etree

from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class Iac(object):
    def __init__(self):
        self.db = self.create_conn('development')
        self.url = ''

    def format_soa_xml(self, iac_xml):
        soa_format_xml = """<sen:SendSupplierCurrentAccountServiceBal xmlns:sen="http://www.foton.com.cn/SendSupplierCurrentAccountBal">
	<sen:DATA>
		<![CDATA[
			<DATA>
				<HEAD>
					<BIZTRANSACTIONID>SAP_SYC_904_2017061010031100</BIZTRANSACTIONID>
					<COUNT>3</COUNT>
					<CONSUMER>SAP</CONSUMER>
					<SRVLEVEL>1</SRVLEVEL>
					<ACCOUNT>SAP</ACCOUNT>
					<PASSWORD>SAP1509030</PASSWORD>
				</HEAD>
				<LIST>
					<ITEM>
						{iac_xml}
					</ITEM>
				</LIST>
			</DATA>
		]]>
	</sen:DATA>
</sen:SendSupplierCurrentAccountServiceBal>"""
        return soa_format_xml.format(iac_xml = iac_xml)

    def dict_to_xml(self, dict_data):
        root = etree.Element('root')
        for k, v in dict_data.items():
            node = etree.SubElement(root, k.capitalize())
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

    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

    def set_to_erp(self, xml):
        try:
            requests.post(
                url = self.url,
                data = xml,
                headers = {
                          'Content-Type': 'text/xml;charset=UTF-8',
              },
            )
        except Exception:
            pass


if __name__ == '__main__':

    iac = Iac()
    dataset = iac.get_iac_data()
    if dataset:
        for data in dataset:
            xml = iac.dict_to_xml(data)
            soa_xml = iac.format_soa_xml(xml)
            # TODO
            # obj.set_to_erp(xml)
