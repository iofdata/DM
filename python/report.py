#!/usr/bin/env python
# encoding: utf-8

import qingcloud.iaas
import api
import json
import time
import iso8601
import price
from sendmail import Mailsender

def check_conn():
    try:
        return qingcloud.iaas.connect_to_zone(api.api['ZONE'],api.api['NAME'],api.api['CODE'])
    except Exception, e:
        print "Thers is something wrong when trying to connect to QingCloud! Please see %s ..." % str(e)

def get_Instances(conn):
    ins_list = []
    for ins in conn.describe_instances(status=["running","stopped"],verbose=1,limit=1000)[u'instance_set']:
        ad = get_info(conn,ins)
        ins_list.append(ad)
    return ins_list

def get_info(conn,ins):
    d = {}
    #d[u'cpu'] = repr(ins[u'vcpus_current']) + 'K'
    cpu = repr(ins[u'vcpus_current']) + 'K'
    #d[u'mem'] = repr(int(ins[ u'memory_current'])/1024) + 'G'
    mem = repr(int(ins[ u'memory_current'])/1024) + 'G'
    d[u'cfg'] = str(cpu) + str(mem)
    #d[u'status'] = ins[u'status']
    d[u'time'] = ins[u'create_time']
    d[u'time'] = time.strftime("%Y-%m-%d",iso8601.parse_date(d[u'time']).timetuple())
    d[u'name'] = ins[u'instance_name']
    #d[u'os'] = ins[u'image'][u'os_family']
    os = ins[u'image'][u'os_family']
    if os == u'windows':
        d[u'p_cfg'] = '%.2f' % price.windows[cpu][mem]
    else:
        d[u'p_cfg'] = '%.2f' % price.centos[cpu][mem]
    if u"eip" in ins:
        d[u'ip'] = ins[u"eip"][u"eip_addr"]
        band = repr(ins[u"eip"][u'bandwidth']) + 'M'
        d[u'band'] = band
        d[u'p_ip'] = '%.2f' % price.net[band]
    else:
        d[u'band'] = "无"
        d[u'p_ip'] = "0"
        if ins[u'instance_name'] == 'dns01':
            d[u'ip'] = "192.168.3.3"
        elif ins[u'instance_name'] == 'dns02':
            d[u'ip'] = "192.168.3.4"
        else:
            d[u'ip'] = ins[u'vxnets'][0][u'private_ip']
    if u"volume_ids" in ins and ins[u"volume_ids"] != []:
        #print ins[u"volume_ids"]
        d[u'vols'] = get_vols(conn,ins[u"volume_ids"])
    else:
        d[u'vols'] = {"price": "0","size": "无","num":0}
    return d

def get_vols(conn,vols):
    vds = {}
    vtype = 0
    vnum = 0
    for vol in conn.describe_volumes(volumes=vols,status=["in-use"],verbose=1)[u"volume_set"]:
        vnum += 1
        if u'type' in vds:
            vtype += int(vol[u"volume_type"])
        else:
            vtype = int(vol[u"volume_type"])
        if u'size' in vds:
            vds[u'size'] += int(vol[u'size'])
        else:
            vds[u'size'] = int(vol[u'size'])
    vds[u'num'] = vnum
    vds[u'size'] = repr(vds[u'size']) + 'G'
    if vtype == 0:
        vds[u'size'] += "性能型"
    else:
        vds[u'size'] += "容量型"
    if vds[u'size'] not in price.volume[str(vtype)]:
        tmp = vds[u'size'].split('G');
        tmp_tmp = '%.2f' % float(int(tmp[0])/100.00)
        tmp_price = '%.2f' % price.volume[str(vtype)]['100G']
        vds[u'price'] = '%.2f' % ( float(tmp_price) * float(tmp_tmp))
        #print tmp_tmp,tmp_price,vds[u'price']
    else:
        vds[u'price'] = '%.2f' % price.volume[str(vtype)][str(vds[u'size'])]
    return vds

def makeHtml(ins_list):
    cp_num,cp_price,ip_num,ip_price,v_num,v_price,t_price = 0,0,0,0,0,0,0
    html = """
<html>
    <head>The resource iformation in {0}!</head>
    <body>
        <p>Table 1. 机器资源列表明细!</p>
        <table border="1">
            <tr>
                <th align="center">日期</th>
                <th align="center">机器名</th>
                <th align="center">IP</th>
                <th align="center">主机配置</th>
                <th align="center">硬盘配置</th>
                <th align="center">带宽</th>
                <th align="center">主机费用</th>
                <th align="center">硬盘费用</th>
                <th align="center">网络费用</th>
            </tr>""".format(api.api['ZONE'])
    for ins in ins_list:
        cp_num += 1
        cp_price += float(ins[u'p_cfg'])
        if ins[u'band'] != "无":
            ip_num += 1
            ip_price += float(ins[u'p_ip'])
        v_num += ins[u'vols'][u"num"]
        v_price += float(ins[u'vols'][u"price"])
        html += """
            <tr>
                <td>{0[time]}</td>
                <td>{0[name]}</td>
                <td>{0[ip]}</td>
                <td>{0[cfg]}</td>
                <td>{0[vols][size]}</td>
                <td>{0[band]}</td>
                <td align="right">{0[p_cfg]}</td>
                <td align="right">{0[vols][price]}</td>
                <td align="right">{0[p_ip]}</td>
            </tr>""".format(ins)
    html += """
        </table>
    <p>Table 2. 汇总!</p>
        <table border="1">
            <tr>
                <th ></th>
                <th align="center">数量</th>
                <th align="center">总价</th>
            </tr>"""
    html += """
            <tr>
                <th >公网</th>
                <td align="right">{0}</td>
                <td align="right">{1}</td>
            </tr>""".format(ip_num,ip_price)
    html += """
            <tr>
                <th >主机</th>
                <td align="right">{0}</td>
                <td align="right">{1}</td>
            </tr>""".format(cp_num,cp_price)
    html += """
            <tr>
                <th >硬盘</th>
                <td align="right">{0}</td>
                <td align="right">{1}</td>
            </tr>""".format(v_num,v_price)
    html += """
            <tr>
                <th >汇总</th>
                <td align="right"></td>
                <td align="right">{0}</td>
            </tr>""".format(v_price + ip_price + cp_price)
    html += """
        </table>
    </body>
</html>
"""
    return html

def mail(ins_list):
    #receiverList = ["tanhao2013@foxmail.com","tanhao2013@me.com"]
    receiverList = api.api['mails']
    mail = Mailsender()
    mail.setSmtpServer("smtp.163.com")
    mail.setSender("peony_wh@163.com","peony_wh","peony2014")
    mail.setReceiver(receiverList)
    mail.setSubject("This is the list of resource in {0}!".format(api.api['ZONE']))
    mail.setText("This is the list of resource in {0}!\nJust for Testing!\nSeeing:".format(api.api['ZONE']))
    mail.setHtml(makeHtml(ins_list))
    mail.sendMail()

def ip2int(s):
    l = [int(i) for i in s.split('.')]
    return (l[0] << 24) | (l[1] << 16) | (l[2] << 8) | l[3]

def test(verbose):
    conn = check_conn()
    #ins_list = sorted(get_Instances(conn),key=lambda ins: ins[u'ip'])
    ins_list = sorted(get_Instances(conn),key=lambda ins: ins[u'ip'],cmp = lambda x, y: cmp(ip2int(x), ip2int(y)))
    #ins_list = sorted(get_Instances(conn),key=lambda ins: ins[u'name'])
    #print json.dumps(ins_list,indent=4)
    mail(ins_list)
    if (verbose != False):
    	print json.dumps(ins_list,indent=4)
    	
def main(args):
	api.api['ZONE'] = args.zone
	test(args.verbose)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(prog='report.py',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-z','--zone',
		choices=['pek2', 'gd1'],
		help="-z pek2 : computers in Beijing;\n-z gd1 : computers in Guangdong.")
	parser.add_argument('-v','--verbose',
		dest='verbose',
		action="store_true",
		default=False,
		help='print information om stdout')
	args = parser.parse_args()
	main(args)
