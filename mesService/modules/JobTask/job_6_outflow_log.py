import sys
import json
import requests
import xmltodict
from lxml import etree
from flask import current_app


sys.path.append(r'/home/test01/mesService')


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class Outflow(object):

    def __init__(self):
        self.db = self.create_conn('development')
        self.url = r'http://soa.bfcec.com/WP_BFCEC_SOA/APP_MSFM_SERVICES/Proxy_Services/TA_EBS/MSFM_BFCEC_052_SendMachiningOrderTrans_PS?wsdl'
        self.url2 = r'http://soa.bfcec.com/WP_BFCEC_SOA/APP_MSFM_SERVICES/Proxy_Services/TA_EBS/MSFM_BFCEC_051_SendIACInterface_PS?wsdl'

    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

    def execteDatabase(self):
        """调用存储过程"""
        sql = "select job_outflow_log();"
        try:
            ret = self.db.query(sql)
            # print(ret)
            return ret[0]['job_outflow_log']
        except Exception as e:
            # current_app.logger.error(traceback.format_exc())
            print(e)

    def set_to_erp(self, xml,datas):
        number = 1
        while True:
            try:
                if datas['transactionid'] =='IAC':
                    # print('IAC123',xml)
                    reqobj = requests.Session()
                    reqobj.auth = ('MSFM', 'MSFM202004210945')
                    response = reqobj.post(
                        url=self.url2,
                        data=xml,
                        headers={
                            'Content-Type': 'application/xml'
                        },
                    )

                    backxml = response.content
                    tree = etree.HTML(backxml)
                    xml_str1 = etree.tostring(tree)
                    # print('backxml', xml_str1)
                    list_data = xmltodict.parse(xml_str1)['html']['body']['envelope']['body'][
                        'getmsfm_bfcec_051_sendiacinterfaceresponse']['message']['outputparameters']['x_return_status']
                    print('list_data', list_data)

                    if list_data == 'S':
                        message = {'application': 'MES',
                                   'transactionid': 'IAC',
                                   'transactiontype': 'IAC回冲',
                                   'message': '回冲成功',
                                   'actionstatus': '修改',
                                   'wiporder': '',
                                   'result': 1,
                                   'context': '',
                                   'createdby': 'admin'
                                   }
                        json_message = json.dumps(message)
                        base_sql = """select updata_outflow_log('{}');"""
                        sql = base_sql.format(json_message)
                        print(sql)
                        result = self.db.query(sql)
                        print(result)
                        break

                    else:
                        number += 1
                        if number == 3:
                            message = {'application': 'MES',
                                       'transactionid': 'IAC',
                                       'transactiontype': 'IAC回冲',
                                       'message': '三次回冲失败',
                                       'actionstatus': '修改',
                                       'wiporder': '',
                                       'result': 3,
                                       'context': '',
                                       'createdby': 'admin'
                                       }
                            json_message = json.dumps(message)
                            print(json_message)
                            base_sql = """select updata_outflow_log('{}');"""
                            sql = base_sql.format(json_message)
                            self.db.query(sql)
                            print('no s')
                            break
                else:
                    print('回冲', datas['transactionid'])
                    print('回冲xml', xml)
                    reqobj = requests.Session()
                    reqobj.auth = ('MSFM', 'MSFM202004210945')
                    response = reqobj.post(
                        url=self.url,
                        data=xml,
                        headers={
                            'Content-Type': 'application/xml'
                        },
                    )

                    backxml = response.content
                    print('backxml', backxml)
                    tree = etree.HTML(backxml)
                    xml_str1 = etree.tostring(tree)
                    print('xml_str1', xml_str1)
                    list_data = xmltodict.parse(xml_str1)['html']['body']['envelope']['body'][
                        'getmsfm_bfcec_052_sendmachiningordertransresponse']['sign'][1]['outputparameters']['x_status_code']
                    print('list_data', list_data)

                    if list_data == 'S':
                        message = {'application': 'MES',
                                   'transactionid': datas['transactionid'],
                                   'transactiontype': datas['transactiontype'],
                                   'message': '回冲成功',
                                   'actionstatus': '修改',
                                   'wiporder': datas['wiporder'],
                                   'result': 1,
                                   'context': '',
                                   'createdby': 'admin'
                                   }
                        json_message = json.dumps(message)
                        base_sql = """select updata_outflow_log('{}');"""
                        sql = base_sql.format(json_message)
                        print(sql)
                        result = self.db.query(sql)
                        print(result)
                        break

                    else:
                        number += 1
                        if number == 3 :
                            message = {'application': 'MES',
                                       'transactionid': datas['transactionid'],
                                       'transactiontype': datas['transactiontype'],
                                       'message': '三次回冲失败',
                                       'actionstatus': '修改',
                                       'wiporder': datas['wiporder'],
                                       'result': 3,
                                       'context': '',
                                       'createdby': 'admin'
                                       }
                            json_message = json.dumps(message)
                            print(json_message)
                            base_sql = """select updata_outflow_log('{}');"""
                            sql = base_sql.format(json_message)
                            self.db.query(sql)
                            print('no s')
                            break

            except Exception:
                break

if __name__ == '__main__':
    wd = Outflow()
    dataset = wd.execteDatabase()

    if dataset:
        for datas in dataset:
            xml = datas['context']
            wd.set_to_erp(xml,datas)

    else:
        print("无需要发送数据")




