#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    @File:      mails.py
    @Author: Hao Tan
    @Date:     20140813
    @Email:  tanhao2013@foxmail.com
    @Desc:  A script for mails sending.
    @Refer to£º http://www.oschina.net/code/snippet_144709_13325
"""

import smtplib
from email.mime.text import MIMEText
import base64

class Mailsender():
    def __init__(self):
        print "Start sending the mails ..."

    def setSmtpServer(self, smtpServer):
        self.smtpserver = smtpServer

    def setSender(self, sender, password):
        self.sender = sender
        self.password = password

    def setReceiver(self,receiver):
        self.receiver = receiver

    def setSubject(self, subject):
        self.subject = subject

    def setContent(self,content):
        self.content = content

    def sendMail(self):
        smtp = smtplib.SMTP(self.smtpserver, 587)
        #smtp.connect(self.smtpserver, 25)
        #smtp.connect(self.smtpserver, 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.sender, self.password)

#        msg = MIMEText(self.content)
#        msg['From'] = self.sender
#        msg['To'] = ",".join(self.receiver)
#        msg['Subject'] = self.subject

        self.content = base64.b64encode(self.content)
        msg = "From:%s\nTo:%s\nSubject:%s\nContent-Type:text/html\nContent-Transfer-Encoding:base64\n\n%s"%(self.sender, self.receiver, self.subject,self.content)

#        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.sendmail(self.sender, self.receiver, msg)
        smtp.quit()

    def __del__(self):
        print "Finish sending mails !"

def main():
    receiverList = ["tanhao2013@me.com","tanhao2013@foxmail.com","tanhao2013@msn.cn"]

    mail = Mailsender()

    mail.setSmtpServer("smtp.gmail.com")
    mail.setSender("tanhao2013@gmail.com", "**********")
    mail.setReceiver(receiverList)
    mail.setSubject("This is a test mail!")
    mail.setContent("I have no content,do you know?\nJust for testing!")

    mail.sendMail()

####
#   import mails
#   mails.Mailsender
####

if __name__ == '__main__':
    main()
