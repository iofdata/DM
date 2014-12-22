#!/usr/bin/env python
# encoding: utf-8

import qingcloud.iaas
from config import api
import json
import time
import yaml
from multiprocessing import Pool

def stop_cluster((conn,cluster)):
        check_cluster(conn,cluster)
        '''
        eips = get_eips(cluster)
        if len(eips) != 0:
                # billing_mode: "bandwidth" or "traffic"
                set_eips_billing_mode(conn,eips,"traffic")
                print "Trying to set %s billing_mode to %s" % (eips,"traffic")
        '''
        ins = get_instances(cluster)
        if len(ins['masters']) != 0:
                print "Trying to stop masters %s " % ins['masters']
                stop_instances((conn,ins['masters']))
                while not is_done(conn,ins['masters'],astatus="stopped"):
                        time.sleep(3)
                print "Trying to stop slavers %s " %  ins['slavers']
                slavers = [[slaver] for slaver in ins['slavers']]
                map(stop_instances,zip([conn]*len(slavers),slavers))
                #stop_instances(conn,ins['slavers'])
                while not is_done(conn,ins['slavers'],astatus="stopped"):
                        time.sleep(5)
        else:
                print "Trying to stop nodes %s " %  ins['slavers']
                slavers = [[slaver] for slaver in ins['slavers']]
                map(stop_instances,zip([conn]*len(slavers),slavers))
                #stop_instances(conn,ins['slavers'])
                while not is_done(conn,ins['slavers'],astatus="stopped"):
                        time.sleep(5)

def start_cluster((conn,cluster)):
        check_cluster(conn,cluster)
        '''
        eips = get_eips(cluster)
        if len(eips) != 0:
                # billing_mode: "bandwidth" or "traffic"
                set_eips_billing_mode(conn,eips,"bandwidth")
                print "Trying to set %s billing_mode to %s" % (eips,"bandwidth")
        '''
        ins = get_instances(cluster)
        if len(ins['masters']) != 0:
                print "Trying to start slavers %s " %  ins['slavers']
                slavers = [[slaver] for slaver in ins['slavers']]
                map(start_instances,zip([conn]*len(slavers),slavers))
                #start_instances(conn,ins['slavers'])
                while not is_done(conn,ins['slavers'],astatus="running"):
                        time.sleep(5)
                print "Trying to start masters %s " % ins['masters']
                start_instances((conn,ins['masters']))
                while not is_done(conn,ins['masters'],astatus="running"):
                        time.sleep(3)
        else:
                print "Trying to start nodes %s " %  ins['slavers']
                slavers = [[slaver] for slaver in ins['slavers']]
                map(start_instances,zip([conn]*len(slavers),slavers))
                #start_instances(conn,ins['slavers'])
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
                if (instance["instance_name"].endswith("-master")) or (instance["instance_name"].endswith("-cobar")):
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
        print "Thers is something wrong when trying to connect to QingCloud! Please see %s ..." % str(e)

def set_eips_billing_mode(conn,eips,billing_mode):
        ret = conn.change_eips_billing_mode(eips, billing_mode)
        if u'ret_code' in ret:
                if ret[u'ret_code'] != 0:
                        print "Change eips billing_mode to %s filled!" % billing_mode


#def stop_instances(conn,instances):
def stop_instances((conn,instances)):
    if is_done(conn,instances,astatus="stopped"):
        print "Instances %s are already stopped!" % repr(instances)
    else:
        ret = conn.stop_instances(instances,force=True)
        if u'ret_code' in ret:
            if ret[u'ret_code'] != 0:
                print "Stop instances %s filled!" % repr(instances)

#def start_instances(conn,instances):
def start_instances((conn,instances)):
    if is_done(conn,instances,astatus="running"):
        print "Instances %s are already running!" % repr(instances)
    else:
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

# hadoop->hbase->memcached,mina,docdb,crTest
def start_pipe(conn,clusters,orders):
    print "We are trying to start these clusters: %s ..." % orders
    for x in eval(str(orders)):
        #pool = Pool(len(x))
        map(start_cluster, zip([conn]*len(x), [clusters[i] for i in list(x)]))
        #pool.map(start_cluster, zip([conn]*len(x), [clusters[i] for i in x]))
        time.sleep(2)
    print "Start pipeline is finished!"

# crTest,docdb,mina,memcached->hbase->hadoop
def stop_pipe(conn,clusters,orders):
    print "We are trying to stop these clusters: %s ..." % orders
    #print conn
    for x in eval(str(orders)):
        y = [clusters[i] for i in list(x)]
        #print y
        #pool = Pool(len(list(x)))
        #print ([conn]*len(x))
        map(stop_cluster, zip([conn]*len(x),y))
        #pool.map(stop_cluster, zip([conn]*len(x),y))
        #pool.join()
        #pool.close()
        #pool.join()
        time.sleep(2)
        #print "****"
    print "Stop pipeline is finished!"

def parser_yaml(fyaml):
        fp = open(fyaml)
        dataMap = yaml.load(fp)
        #print json.dumps(dataMap,indent=4)
        clusters = {}
        for (cluster_name,cluster_pcs) in dataMap.iteritems():
                clusters[cluster_name] = []
                for (name,ip) in cluster_pcs.iteritems():
                        dtmp = {}
                        dtmp[u'instance_name'] = name
                        if ip.startswith("192"):
                                dtmp[u'private_ip'] = ip
                        else:
                                dtmp[u'eip_addr'] = ip
                        clusters[cluster_name].append(dtmp)
        #print json.dumps(clusters,indent=4)
        #print dataMap
        return clusters

def main(args):
    conn = check_conn()
    clusters = parser_yaml(args.yaml)
    if args.command == 'start':
        start_pipe(conn,clusters,args.order)
    else:
        stop_pipe(conn,clusters,args.order)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='cluster_manager.py',
            formatter_class=argparse.RawTextHelpFormatter)
    #command
    parser.add_argument('-c','--command',
            choices=['start', 'stop'],
            required=True,
            help="-c start : start the clusters;\n-c stop : stop  the clusters.")
    #yaml
    parser.add_argument('-y','--yaml',
            required=True,
            help="-y cluster.yaml : a clusters config file with pc name and ip in yaml format.")
    #order
    parser.add_argument('-o',"--order",
            help="-o [[\"index_6_masters\"]] : The cluster shutdown or start order\n\
    a list of list in cluster order, the same clusters in a list have no orders\n\
    such as :\n\
            \'[[\"crTest\",\"docdb\",\"memcached\",\"mina\"],[\"hbase\"],[\"hadoop\"]\'\n\
            \'[[\"index_6_masters\"]]\'\n\
            \'[[\"index_6_masters\",\"index_6_apps\"]]\'\n\
            \'[[\"hadoop\"],[\"hbase\"],[\"crTest\",\"docdb\",\"memcached\",\"mina\"]]\'")
    #ZONE
    '''
    parser.add_argument('-z','--zone',
            choices=['pek2', 'gd1'],
            #required=True,
            help="-z pek2 : clusters in Beijing;\n-z gd1 : clusters in Guangdong.")
    '''
    args = parser.parse_args()
    #print args
    #parser_yaml(args.yaml)
    main(args)
