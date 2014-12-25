#!/usr/bin/env python
import socket

'''
    @Author: Hao Tan
    @Date:   2012-12-25
    @Email:  tanhao2013@foxmail.com
    @Desc:   A short script for ip and port checking!
    @Usage:  python port.py  --ip 119.254.110.32 -p 3306
'''

def isPortOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip,int(port)))
        print 'Your port %s:%s is working!' % (ip,port)
        return True
    except Exception,e:
        print  "Your port %s:%s is failed! Details here: %s"  % (ip,port,str(e))
        return False
    s.close()

def test():
    isPortOpen('127.0.0.1',3306)

def main(args):
    isPortOpen(args.ip,args.port)

if __name__ == '__main__':
    #print "Usage: python port.py  --ip 119.254.110.32 -p 3306"
    import argparse
    parser = argparse.ArgumentParser(prog='port.py',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--ip',
            required=True,
            help="-i 127.0.0.1 the ip to test with!")
    parser.add_argument('-p','--port',
            required=True,
            help="-p 3306 the port to test with!")
    args = parser.parse_args()
    main(args)
