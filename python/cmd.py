#!/usr/bin/env python
# encoding: utf-8

"""	
	@File:   cmd.py   
	@Author: Hao Tan
	@Date:   2014-12-06 
	@Email:  tanhao2013@foxmail.com
	@Desc:   A short script for stop and start cluster in patch.
"""

"""
depend on qingcloud-sdk
pip install qingcloud-sdk
https://docs.qingcloud.com/sdk/python/index.html
"""

"""  config.py
api = {
	'NAME':'XXXXXXXXXXXXXX',
	'CODE':'PPPPPPPPPPPPPP',
    'ZONE':'ZZZ'
}

crTest = [
    {
        "instance_name":"cccccc",
        "private_ip": "192.x.x.x"
    }, 
    ...
    ,
    {
        "instance_name":"cccccc",
        "private_ip": "192.x.x.x"
    }
]

mina = [
    {
        "instance_name":"cccccc",
        "private_ip": "192.x.x.x"
    }, 
    ...
    ,
    {
        "instance_name":"cccccc",
        "private_ip": "192.x.x.x"
    }
]
"""

import qingcloud.iaas
from config import crTest,mina,memcached,hadoop,hbase,api
import json
import time
from multiprocessing import Pool

def stop_cluster(conn,cluster):
	check_cluster(conn,cluster)
	'''
	eips = get_eips(cluster)
	if len(eips) != 0:
		# billing_mode: "bandwidth" or "traffic"
		set_eips_billing_mode(conn,eips,"traffic")
		print "Tring to set %s billing_mode to %s" % (eips,"traffic")
	'''
	ins = get_instances(cluster)
	if len(ins['masters']) != 0:
		print "Tring to stop masters %s " % ins['masters']
		stop_instances(conn,ins['masters'])
		while not is_done(conn,ins['masters'],astatus="stopped"):
			time.sleep(3)
		print "Tring to stop slavers %s " %  ins['slavers']
		stop_instances(conn,ins['slavers'])
		while not is_done(conn,ins['slavers'],astatus="stopped"):
			time.sleep(5)
	else:
		print "Tring to stop nodes %s " %  ins['slavers']
		stop_instances(conn,ins['slavers'])
		while not is_done(conn,ins['slavers'],astatus="stopped"):
			time.sleep(5)

def start_cluster(conn,cluster):
	check_cluster(conn,cluster)
	'''
	eips = get_eips(cluster)
	if len(eips) != 0:
		# billing_mode: "bandwidth" or "traffic"
		set_eips_billing_mode(conn,eips,"bandwidth")
		print "Tring to set %s billing_mode to %s" % (eips,"bandwidth")
	'''
	ins = get_instances(cluster)
	if len(ins['masters']) != 0:
		print "Tring to start slavers %s " %  ins['slavers']
		start_instances(conn,ins['slavers'])
		while not is_done(conn,ins['slavers'],astatus="running"):
			time.sleep(5)
		print "Tring to start masters %s " % ins['masters']
		start_instances(conn,ins['masters'])
		while not is_done(conn,ins['masters'],astatus="running"):
			time.sleep(3)
	else:
		print "Tring to start nodes %s " %  ins['slavers']
		start_instances(conn,ins['slavers'])
		while not is_done(conn,ins['slavers'],astatus="running"):
			time.sleep(5)

def get_eips(cluster):
	eips = []
	for instance in cluster:
		if "eip_id" in instance:
			eips.append(instance["eip_id"])
	return eips

def get_instances(cluster):
	ins = {'masters':[],'slavers':[]}
	for instance in cluster:
		if instance["instance_name"].endswith("-master"):
			ins['masters'].append(instance["instance_id"])
		else:
			ins['slavers'].append(instance["instance_id"])
	return ins

def check_cluster(conn,cluster):
	for instance in cluster:
		check_instance(conn,instance)
	return json.dumps(cluster,indent=4)

def check_instance(conn,d):
	name = d["instance_name"]
	ret = conn.describe_instances(search_word=name,status=["running","stopped"])[u'instance_set']
	for ins in ret:
		d["instance_id"] = ins[u'instance_id']
		if (u'eip' in ins) and ("eip_addr" in d):
			if ins[u'eip'][u'eip_addr'] != d["eip_addr"]:
				print "Your pc name %s maybe wrong with public ip %s" % (name,d["eip_addr"])
				d["eip_addr"] = ins[u'eip'][u'eip_addr']
			d["eip_id"] = ins[u'eip'][u'eip_id']
		if (u'vxnets' in ins) and ("private_ip" in d):
			if (ins[u'vxnets'])[0][u'private_ip'] != d["private_ip"]:
				print "Your pc name %s maybe wrong with private ip %s" % (name,d["private_ip"])
				d["private_ip"] = (ins[u'vxnets'])[0][u'private_ip']

def check_conn():
	try:
		return qingcloud.iaas.connect_to_zone(api['ZONE'],api['NAME'],api['CODE'])
	except Exception, e:
		print "Thers is something wrong when trying to connect to QingCloud! Please see ..."
		print str(e)

def set_eips_billing_mode(conn,eips,billing_mode):
	ret = conn.change_eips_billing_mode(eips, billing_mode)
	if u'ret_code' in ret:
		if ret[u'ret_code'] != 0:
			print "Change eips billing_mode to %s filled!" % billing_mode

def stop_instances(conn,instances):
	ret = conn.stop_instances(instances,force=True)
	if u'ret_code' in ret:
		if ret[u'ret_code'] != 0:
			print "Stop instances %s filled!" % repr(instances)

def start_instances(conn,instances):
	ret = conn.start_instances(instances,force=True)
	if u'ret_code' in ret:
		if ret[u'ret_code'] != 0:
			print "Stop instances %s filled!" % repr(instances)

def is_done(conn,instances,astatus="stopped"):
	ret = conn.describe_instances(instances)[u'instance_set']
	rstatus = True
	for ins in ret:
		if ins[u'status'] != astatus:
			print "%s is still %s" % (ins[u'instance_name'],ins[u'status'])
			rstatus = rstatus and False
	return rstatus

# hbase->hadoop->memcached,mina,crTest
def start_pipe(conn):
    print "We are tring to start these clusters: hbase->hadoop->memcached,mina,crTest ..."
    for y in [hbase,hadoop]:
        start_cluster(conn,y)
        time.sleep(3)
    for x in [memcached,mina,crTest]:
        start_cluster(conn,x)
        time.sleep(2)
    print "Start pipeline is finished!"

# memcached,mina,crTest->hbase->hadoop
def stop_pipe(conn):
    print "We are tring to stop these clusters: memcached,mina,crTest->hbase->hadoop ..."
    for x in [crTest,mina,memcached]:
        stop_cluster(conn,x)
        time.sleep(2)
    for y in [hadoop,hbase]:
        stop_cluster(conn,y)
        time.sleep(3)
    print "Stop pipeline is finished!"

def main(args):
    conn = check_conn()
    if args.c == 'start':
    	start_pipe(conn)
    else:
    	stop_pipe(conn)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='cmd.py',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c',
            choices=['start', 'stop'],
            required=True,
            help="-c start : start the clusters!\n-c stop  : stop  the clusters!")
    args = parser.parse_args()
    #print args.c
    main(args)
