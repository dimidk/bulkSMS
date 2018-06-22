#!/usr/bin/python
#-*- coding: utf-8-*-


import urllib
import datetime
import init
import time
import readStoixeia
from readStoixeia import StudentsStoixeia
from readAbsences import StudentsAbsences
import readAbsences



def sendSMS(i,to,fromSender,name,text,text1,absences):
	
	urlsms_sender=init.urlsms+'to='+to
	urlsms_sender=urlsms_sender+'&from='+fromSender+'&text='+text+name+' '+text1+absences+"&type=xml"

	try:
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':send SMS for student ' + name+'\n')
		
		print "send sms to ",to
				
		"""result=urllib.urlretrieve(urlsms_sender)"""
					
	except:

		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':SMS for student ' + name+' not send successfull\n')
		


def sendSMSAll(i):
	
	tmp=0
	for key,value in StudentsStoixeia.Studentstoixeia.items():
		tmpStoixeia=StudentsStoixeia.Studentstoixeia.get(key)
		init.toSend=tmpStoixeia[2]

		
		if StudentsAbsences.Studentsabsences.has_key(key):
			tmpAbs=StudentsAbsences.Studentsabsences.get(key)
			
			init.studentName=tmpAbs[0]+' '+tmpAbs[1]
			
			init.numberOfAbsences=str(tmpAbs[2])
			

				
			sendSMS(i,init.toSend,init.fromSender,init.studentName,init.text,init.text1,init.numberOfAbsences)
				
