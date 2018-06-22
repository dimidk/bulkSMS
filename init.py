#!/usr/bin/python
#-*- coding: utf-8 -*-

import codecs
import datetime

def get_datetime():
	
	now=str(datetime.datetime.now())
	now_date=now.split(' ')[0]
	now_time=now.split(' ')[1].split('.')[0]
	
	return now_date,now_time


urlsms="https://easysms.gr/api/sms/send?key=72416f5e5edecd&"
toSend=''
fromSender="epalMoiron"
text="Συνολικές απουσίες "
text1=" μέχρι σήμερα : "
studentName=''
numberOfAbsences=''

urlDict={'to':toSend,'from':fromSender,'text':text,'number':numberOfAbsences}
urlFormat="https://easysms.gr/api/sms/send?key=72416f5e5edecd&{to}"

"""urlsms="https://easysms.gr/api/sms/send?key=72416f5e5edecd&to=6938802532&from=epal&text=HelloDimi&type=xml"""

log_file="log_sms.txt"
stoixeiaDir="./stoixeia"
absencesDir="./absences"
fp_log=codecs.open(log_file,'a+')
