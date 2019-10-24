
import code,sys

from mesService.lib.pgwrap.db import connection

if __name__ == '__main__':
    db_info = {
        'database': 'flxuser1',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'huanglg.top',
        'port': 5433,
    }
    cursor = connection()
    res = cursor.query("select * from employee")
    print(res)
    code.interact(local=locals())
