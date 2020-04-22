# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28
# @author  : 郭辉
# @email: hui.guo@mabotech.com

import json
import xmltodict
from lxml import etree
from flask import request
from flask import current_app
from mesService import create_app
from mesService import create_conn
class SequenceInterface:
    db = None

    def __init__(self, itype):
        self.db = create_conn(itype)

    # 定义XML中的排序对象
    sequenceXmlObj = {
        'transactionid': '',                        #固定值
        'status': '',                               #I插入U更新N删除
        'wipjobno': '',                              #工单号
        'sequencenumber': '',                       #排序序列
        'plantcode': '',                            #工厂代码
        'batchid': '',                              #批次
    }

    # 定义数据库中的排序对象 Wip_Sequence
    sequenceDatabaseObj = {
        'TransactionID':'',                   #固定值,区分发送哪个系统
        'status':'',                          #I插入U更新N删除
        'wiporderno': '',                    #工单编号
        'externalIndex': '',                   #原始序号
        'batchid': '',                       #批次
        'facility':'',                        #工厂代码
        'RequestData':''                    # 后端传输原数据
    }

    # 将XML数据与Database字段对应绑定  数据流向 XML--->数据库
    def bindXmlSequenceDatabase(self):
        self.sequenceDatabaseObj['TransactionID'] = self.sequenceXmlObj['transactionid']              #固定值,区分发送哪个系统
        self.sequenceDatabaseObj['status'] = self.sequenceXmlObj['status']                             #I插入U更新N删除
        self.sequenceDatabaseObj['wiporderno'] = self.sequenceXmlObj['wipjobno']                      #工单号
        self.sequenceDatabaseObj['externalIndex'] = self.sequenceXmlObj['sequencenumber']            #序号
        self.sequenceDatabaseObj['facility'] = self.sequenceXmlObj['plantcode']                      #工厂代码
        self.sequenceDatabaseObj['batchid'] = self.sequenceXmlObj['batchid']                         #批次号

    # 从XML文件中解析数据并将其转换为数据库字段
    def analysisFromXML(self,xml_data,xml_body):
        # 解析XML
        # xml_str = request.data
        # print(xml_str)
        try:
            tree = etree.HTML(xml_data)
            xml_str1 = etree.tostring(tree)

            list_data = xmltodict.parse(xml_str1)['html']['body']['data']['seqdwnload']
            # print(list_data)
            wiporderDatabaselist = []
            for key, val in list_data.items():
                # print(key, val)
                self.sequenceXmlObj[key] = val
            self.bindXmlSequenceDatabase()
            self.sequenceDatabaseObj['RequestData'] = str(xml_data, 'utf-8')
            wiporderDatabaselist.append(self.sequenceDatabaseObj.copy())
            # print(wiporderDatabaselist)
            return wiporderDatabaselist
        except:
            result = {
                "status": "error",
                "message": "解析失败,报文格式不正确"
            }
            return json.dumps(result)

    def insertDatabase(self, wiporderDatabaselist):
        json_data = json.dumps(wiporderDatabaselist)
        # print(json_data)

        # 创建sql语句
        base_sql = """select plv8_insert_sequence('{}');"""
        sql = base_sql.format(json_data)
        print(sql)
        # 调用数据库函数

        result = self.db.query(sql)
        sql_result = result[0].get('plv8_insert_sequence')
        print(sql_result)

        return sql_result
