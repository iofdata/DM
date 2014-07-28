#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""	
	@File:      
	@Author: Hao Tan
	@Date:     
	@Email:  tanhao2013@foxmail.com
	@Desc:
"""

import sys

def connect():  #TODO 参数化
	connect = MySQLdb.connect(db = "test",
                        host = "localhost",
                        user = "root",
                        passwd = "123456")
             # Non-local TCP/IP 
        	'''
        	connect = MySQLdb.connect(db = "test",
                        host = "mysql.example.com",
                        port = 3307,
                        user = "root",
                        passwd = "123456")
       	 '''

def main():
	try:
		conn = connect()
		print "Connected!"
		conn.close()
		print "Disconnected"
	except MySQLdb.Error, e:
		raise e
		print "Cannot connect to server"
		print "Error code:" e.args[0]
		print "Error message:" e.args[1]
		sys.exit(1)

if __name__ == '__main__':
	main()
