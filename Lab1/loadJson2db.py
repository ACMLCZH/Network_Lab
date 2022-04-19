import json
from posixpath import curdir
import pymysql

conn = pymysql.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = '111111',
        db = 'lab1',
        charset = 'utf8',
    )
cur = conn.cursor()

path1 = "C:/Users/X/Desktop/计网/lab1/test.json"
dic = {}
with open(path1) as f:
    dic=json.load(f)

keys = ', '.join(dic.keys())
valuesList = [dici for dici in dic.values()]
for index1, value1 in enumerate(valuesList):
    if isinstance(value1, list):
        valuesList[index1] = str(value1)
valuesTuple = tuple(valuesList)

values = ', '.join(['%s']*len(dic)) 
table="test"
print(values)

sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)  

cur.execute(sql,valuesTuple)
conn.commit()
conn.close()
