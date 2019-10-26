# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com


from lxml import etree


class IacToXml(object):
    def __init__(self):
        self.root = etree.Element('root')

    def dict_to_xml(self, dict_data):
        for d in dict_data:
            item = etree.SubElement(self.root, 'item')
            for k, v in d.items():
                # print(k, v)
                try:
                    item.set('name', k)
                    item.set('value', v)
                except Exception as e:
                    pass

        tree = etree.ElementTree(self.root)
        tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    data = [{'TransactionID': 'POF'}, {'PCID': '1000010010'},
            {'PCOID': '1000020010'}, {'PCCID': '1000030010'},
            {'Level1No': '5271866'}, {'ParentNo': '5271867'},
            {'ChildNo': '5568155'}, {'Qty': '1'},
            {'WorkStation': '47500'}, {'EffectiveDate': '2019-9-11 00:00'},
            {'DiscontinueDate': '2019-9-22 00:00'},
            {'ProductionLineNo': '15'}, {'KittingStation': '0'},
            {'BulkWorkStation': '0'}, {'BuildVar': '0'},
            {'PlantCode': 'ISF'}, {'Dummy1': None},
            {'Dummy2': None}, {'Dummy3': None}]
    obj = IacToXml()
    obj.dict_to_xml(data)
