# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28 18:03
# @author  : Huanglg
# @fileName: constants.py
# @email: luguang.huang@mabotech.com

# 版本控制
URL_PREFIX = '/api/v1/'

# api返回值
RET = {
    'status': 200,
    'msg': 'success'
}

# 物料类型
PRODUCTINVENTORYTYPE_ENUM = {
    'BFCEC_半成品': 110,
    'BFCEC_采购件': 120,
    'BFCEC_零件虚拟件': 130,
    'BFCEC_通用类型': 100
}

# 传输给ERP的地址
ERP_HOST = 'http://127.0.0.1:5001'

# BOM物料类型
BOM_ENUM = {
    'BFCEC_采购件': 1,
    'BFCEC_零件虚拟件': 2,
    'BFCEC_é\x87\x87è´\xadä»¶': 1,
    'BFCEC_é\x9b¶ä»¶è\x99\x9aæ\x8b\x9fä»¶': 2,
}

# 物料状态(New：预留默认为1)
STATUS_ENUM = {
    "Active": 1,
    "New": 1,
    "Inactive": 0
}

# 偏离类型(A:增加或者D:删除)
ACTIONS_ENUM = {
    "A": 1,
    "D": 0
}


