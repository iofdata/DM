# -*- coding: UTF-8 -*-
import sys
import MySQLdb

def main():
	try:
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
		print "Connected"
	except :
		print "Can not connect to server"

if __name__ == '__main__':
	main()