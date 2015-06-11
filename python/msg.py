#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    @File:   msg.py
    @Author: Hao Tan
    @Date:
    @Email:  tanhao2013@foxmail.com
    @Desc:
"""

import sys
import httplib
import urllib
import re
import time
import json
import urllib2
from urllib import quote

reload(sys)
sys.setdefaultencoding('utf-8')

"""
    http API: http://124.173.70.59:8081/SmsAndMms/mt?Sn=xxx&Pwd=xxx&mobile=13010203040&content=123

    Sn：用户名 

    Pwd：密码 

    mobile：目的手机号，多条请用英文逗号隔开，最多100个号码

    content：发送内容，如果含有空格，百分数等特殊内容，请用UTF-8编码进行传送，最多300个文字（1个英文或数字也算1个文字）

    响应： <intxmlns="http://tempuri.org/">0</int>
            0   发送成功
            -1  用户名或密码错误
            -2  余额不足
            -3  内容超过300字
            -4  IP不符合
            -404    系统异常
"""

#urllib2.urlopen(url, urllib.urlencode(data))
class WebSendSmsClient(object):
    """
    desc:       WebSendSmsClient for http API
    attribute:  mobile,content
    """
    def __init__(self, mobile, content):
        super(WebSendSmsClient, self).__init__()
        self.mobile       = mobile
        self.content      = content
        self.__username   =""
        self.__password   =""
        self.__serviceURL =""

    def getBalance(self):
        url_address = self.__serviceURL + "/balance?" \
                 + "Sn="      + self.__username \
                 + "&Pwd="    + self.__password
        return urllib.urlopen(url_address).read()

    def format_url(self):
        url_address = self.__serviceURL + "/mt?" \
            + "Sn="      + self.__username \
            + "&Pwd="    + self.__password \
            + "&mobile=" + self.mobile \
            + "&content="+ self.content
        return url_address

    def SendMsg(self):
        # call the api by http get method
        url = self.format_url()
        print url
        req = urllib2.Request(url)
        con = urllib2.urlopen(req).read()
        print con
        """
        text = urllib2.urlopen(url)
        response = urllib.request.urlopen(quote(self.format_url())) 
        pat = r'<int xmlns=\"http://tempuri.org/\">(.*)</int>'
        print text
        print response
        print text.read()
        print response.read()
        m = re.search(pat,text)
        if m :
            return m.group(1)
        else:
            return 1
        """

def msg2log(res, tel, msg):
    print  res
    logfile = open('msg.log', 'a')
    now = time.strftime('%Y%m%d %H:%M:%S')
    now += '\t' + tel + '\t' + msg

    if res == '0':
        logfile.write(now + '\tSendMsg Done!\n')
    elif res == '1':
        logfile.write(now + '\tSendMsg Failed! Please check it!\n')
    elif res == '-1':
        logfile.write(now + '\tSendMsg Failed! 用户名或密码错误!\n')
    elif res == '-2':
        logfile.write(now + '\tSendMsg Failed! 余额不足!\n')
    elif res == '-3':
        logfile.write(now + '\tSendMsg Failed! 内容超过300字!\n')
    elif res == '-4':
        logfile.write(now + '\tSendMsg Failed! IP不符合!\n')
    else:
        logfile.write(now + '\tSendMsg Failed! 系统异常!\n')
    logfile.close()


def test():
    print "This is a test massege to 18502705665"
    print "Here we go ... !"

    mobile = "18502705665"
    content = quote("磁盘IO>120")
    job = WebSendSmsClient(mobile, content)
    answer = job.SendMsg()
    print "余额短信条数：%s" % job.getBalance().strip("\r\n")
    msg2log(answer, mobile, content)

def main():
    print "Test begin ... !"
    test()
    print "Test doen!"

if __name__ == '__main__':
    main()
