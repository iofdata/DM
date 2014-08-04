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
import getopt
import MySQLdb

try:
	opts, args = getopt(sys.argv[1:],
		"h:p:u",
		["host=", "password=", "user="])
except getopt.error, e:
	print "%s: %s" (sys.argv[0],e)
	sys.exit(1)

host_name = password = user_name = ""

for opt, arg in opts:
	if opt in ("-h", "-host"):
		host_name = arg
	elif opt in ("-p", "-password"):
		password = arg
	elif opt in ("-u","--user"):
		user_name = arg

try:
	conn = MySQLdb.connect(
		db = "cookbook",
		host = host_name,
		user = user_name,
		passwd = password
		)
	print "Connected!"
except Exception, e:
	print "Can not connect to server!"
	print "Error:", e.args[1]
	print "Code:", e.args[0]
	sys.exit(1)

conn.close()
print "Disconnected!"
