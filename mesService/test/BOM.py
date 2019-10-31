# -*- coding: utf-8 -*-
# @createTime    : 2019/10/22 20:59
# @author  : Huanglg
# @fileName: BOM.py
# @email: luguang.huang@mabotech.com
import time
from mesService.lib.OracleLib.OracleDBUtil import Oracle

def print_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print('current Function [%s] run time is %.2f' % (func.__name__ ,time.time() - local_time))
    return wrapper

@print_run_time
def test_oracle():
    oracle = Oracle()
    product_sql = """select id productid, tt.medium productdesc from product p
left join TEXT_TRANSLATION tt on p.textid = tt.textid and tt.LANGUAGEID = 2052"""
    products = oracle.query(product_sql)
    print(products)
    product_component_sql = """select PC.COMPONENTID,TT.MEDIUM,PC.PRODUCTID PRODUCTID,C.PRODUCTID CPRODUCTID from PRODUCT_COMPONENT PC 
left join COMPONENT C on C.ID = PC.COMPONENTID
left join PRODUCT P on P.ID = C.PRODUCTID
left join TEXT_TRANSLATION TT on TT.TEXTID = P.TEXTID and TT.LANGUAGEID = 2052
where PC.PRODUCTID={productid}"""
    for product in products:
        productid = product['productid']
        sql = product_component_sql.format(productid=productid)
        product_component = oracle.query(sql)
        print(product_component)


if __name__ == '__main__':
    test_oracle()
