#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""    
    @File:      
    @Author: Hao Tan
    @Date:     
    @Email:  tanhao2013@foxmail.com
    @Desc: 这是一个登录服务器的自动ssh脚本 ,需要安装pexpect module
"""

import os  
import sys  
import pexpect  
import string  
  
"""
SERVERS = {
    "502" :["192.168.5.2","root", "Mdbjgst2014"],
    "503" :["192.168.5.2","root", "Mdbjgst2014"],
    "504" :["192.168.5.2","root", "Mdbjgst2014"],
    "505" :["192.168.5.2","root", "Mdbjgst2014"],
    "506" :["192.168.5.2","root", "Mdbjgst2014"],
    "507" :["192.168.5.2","root", "Mdbjgst2014"],
    "508" :["192.168.5.2","root", "Mdbjgst2014"],
    "509" :["192.168.5.2","root", "Mdbjgst2014"],
    "510" :["192.168.5.2","root", "Mdbjgst2014"],
    "511" :["192.168.5.2","root", "Mdbjgst2014"],
    "512" :["192.168.5.2","root", "Mdbjgst2014"],
    "513" :["192.168.5.2","root", "Mdbjgst2014"],
    "514" :["192.168.5.2","root", "Mdbjgst2014"],
    "515" :["192.168.5.2","root", "Mdbjgst2014"],
    "516" :["192.168.5.2","root", "Mdbjgst2014"],
    "517" :["192.168.5.2","root", "Mdbjgst2014"],
    "518" :["192.168.5.2","root", "Mdbjgst2014"],
    "519" :["192.168.5.2","root", "Mdbjgst2014"],
    "520" :["192.168.5.2","root", "Mdbjgst2014"]
}
"""

public_ip = "119.254.110.32"
usr           = "root"      
  
def auto_connect():  
    """ 
    自动登录实现,提供选择功能 
    """  
    while True:  
        print "\n\n###########################################################"  
        for server in Server_Ip.keys():  
            print "["+server+"]=>"+"["+Server_Ip[server][0]+"]"+" [服务器用途]=>"+"["+Server_Ip[server][3]+"]"  
        print "###########################################################\n"  
        destination=raw_input("[forest,which server do you want to connect?]=>")  
         
        if(Server_Ip.has_key(destination)):  
            print "\n正在连接服务器"+destination  
            break  
        else:  
            print "\n服务器没有添加到列表中"  
            return  
    URL="ssh %s@%s"%(Server_Ip[destination][1],Server_Ip[destination][0])  
#   print URL  
#   发起连接进程    
    try:  
        p=pexpect.spawn(URL)  
        if Server_Ip[destination][2] != "":
            p.expect("password:")
            p.sendline(Server_Ip[destination][2]+"\n")
        p.interact()  
    except:  
        print "关闭连接"  
auto_connect()  