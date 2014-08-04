#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""    
    @File:      
    @Author: Hao Tan
    @Date:     
    @Email:  tanhao2013@foxmail.com
    @Desc: 这是一个登录服务器的自动ssh脚本 ,需要安装pexpect module
"""



#!/usr/bin/python  
#  coding=utf-8  
#   这是一个登录服务器的自动ssh脚本 ,需要安装pexpect module
#   
#  
# @created on 2012.3.7 5:56 am  
#  
import os  
import sys  
import pexpect  
import string  
  
Server_Ip={  
  
    "主机代号":["主机IP地址","登录账户","密码","服务器用途"]  
#   在此处添加主机列表      
}  
  
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