# import json
# from posixpath import curdir
import pymysql


class Server_SQL:
    def __init__(self, port=3306, password="111111"):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=port,
            user='root',
            passwd=password,
            db='lab1',
            charset='utf8',
        )
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def send_data(self, data: dict, table="server_data"):
        keys = ', '.join(data.keys())
        valuesList = [dici for dici in data.values()]
        for index1, value1 in enumerate(valuesList):
            if isinstance(value1, list):
                valuesList[index1] = str(value1)
        valuesTuple = tuple(valuesList)
        values = ', '.join(['%s'] * len(data))
        print(values)
        sql = 'REPLACE INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        self.cur.execute(sql, valuesTuple)
        self.conn.commit()

    def close(self):
        self.conn.close()




