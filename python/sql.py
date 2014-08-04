#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
1 python DBI 数据库连接对象的获得一个游标对象；
2 游标的execute()向服务器发送语句，抛出异常或返回结果集
"""


## 	A 不返回结果
##	INSERT
##	DELETE
##	UPDATE
cursor = conn.cursor()
cursor.execute("UPDATE profile SET cats = cats + 1 WHERE name = 'Fred'")
print "Number of rows updated: %d" % cursor.rowcount
cursor.close()


## 	B 返回结果
##	SELECT
##	SHOW
##	EXPLAIN
##	DESCRIBE
##	fetchone() 顺序返回下一行
cursor = conn.cursor()
cursor.execute("SELECT id, name, cats FROM profile")
while 1 :
	row = cursor.fetchone() #len(row)
	if row == None :
		break
	print "id: %s, name: %s, cats:%s" % (row[0],row[1],row[2])
print "Number of rows returned: %d" % cursor.rowcount
cursor.close()

##	fetchall() 行序列方式返回整个结果集
cursor = conn.cursor()
cursor.execute("SELECT id, name, cats FROM profile")
rows= cursor.fetchall() #len(rows) 
for row in rows:  #rows[1][2]
	print "id: %s, name: %s, cats:%s" % (row[0],row[1],row[2])
print "Number of rows returned: %d" % cursor.rowcount
cursor.close()


##	DictCursor通过列名来访问行值
cursor = conn.cursor(MySQLdb.cursor.DictCursor)
cursor.execute("SELECT id, name, cats FROM profile")
for row in cursor.fetchall():
	print "id: %s, name: %s, cats:%s" % (row[0],row[1],row[2])
print "Number of rows returned: %d" % cursor.rowcount
cursor.close()