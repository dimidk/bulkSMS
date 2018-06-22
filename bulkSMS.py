#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import string
import urllib
import os
import datetime
import init
import sendingSMS
import xlrd
import time
import readStoixeia
from readStoixeia import StudentsStoixeia
from readAbsences import StudentsAbsences
import readAbsences


"""διαβάζει κατάσταση excell με στοιχεία μαθητή και δημιουργεί λεξικό. διαβάζει κατάσταση excell με απουσίες μαθητή και δημιουργεί λεξικό
τρέχει ως υπηρεσία και μόλις διαπιστώσει νέα αντίστοιχα αρχεία στους φακέλους κάνει ενημέρωση τα λεξικά.αν ενημερωθεί το λεξικό των
απουσιών, στέλνει sms με απουσίες. γράφει στο log αρχείο όσο η υπηρεσία τρέχει."""


"""result=urllib.urlretrieve(urlsms)"""



now=init.get_datetime()
init.fp_log.write(now[0]+' '+now[1]+':Start application\n')

				
				
def filesExist(a,filesDir):
	
	flag=0
	for root,dirs,filenames in os.walk(filesDir,topdown=True):
		for name in filenames:
			print name
			if name.find('prc')>0:
				flag+=1
	print "flag",flag				
	if flag==len(filenames):
		 a=True
	else:
		a=False
	return a


def findFile(filesDir):
	
	flag=0
	a=False

	for root,dirs,filenames in os.walk(filesDir,topdown=True):
		listall=[name for name in filenames if name.find('xls.prc')!=-1]
		sublist=[name for name in filenames if name not in listall]
	
	return sublist	
	
		
	
if __name__== '__main__':
	
	
	
	print "Start sms application"
	print "First read students' information"
		
	i=0
	a,b=False,False
	a=filesExist(a,init.stoixeiaDir)			
	b=filesExist(b,init.absencesDir)

	
	while True:
		if i==0 and not a and not b:
			
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':-------------------------------------------\n')
			
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':First time read Students information'+'\n')
			readStoixeia.read_files()
			print "testing delay time"
			time.sleep(5)
			print "end of sleep"
		
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':Then first time read Absences Students file'+ '\n')
			readAbsences.read_files()
			
			print "testing delay time"
			time.sleep(5)
			print "end of sleep"
			
			sendingSMS.sendSMSAll(i)
			i+=1
		else:
			a,b=False,False
			a=filesExist(a,init.stoixeiaDir)
			print "stoixeiaDir",a
			
			b=filesExist(b,init.absencesDir)
			print "absencesDir",b
			
			print "sleep 5"
			time.sleep(5)
			if a and b:
				print "a and b sleep 10"
				i+=1
				
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+':no new absences and information files\n')
				
				time.sleep(5)
				continue
				
			elif a and not b:
				
				"""this is crucial, if absences dictionary is created must not recreate"""
				
				print "a and not b "				
															
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+':new absences files. Change the dictionary\n')
				
				newfiles=findFile(init.absencesDir)
				for name in newfiles:
					
					now=init.get_datetime()
					init.fp_log.write(now[0]+' '+now[1]+':delete absences file\n')
					filename=init.absencesDir+'/'+name+'.prc'
					os.remove(filename)
					
					print name
					print filename
					
					now=init.get_datetime()
					init.fp_log.write(now[0]+' '+now[1]+':update process file\n')
					
					filename=init.absencesDir+'/'+name
					readAbsences.update_dict(filename)
				
					now=init.get_datetime()
					init.fp_log.write(now[0]+' '+now[1]+':send sms\n')
				
				
				i+=1
				print "second time running length",len(StudentsAbsences.Studentsabsences)
				time.sleep(5)
				"""don't have to see if not a and b or not a and not b 'cause either i have to change student's information"""
			
			else:
				"""find which information file is xls"""
				
				print "anything else sleep 5"
				i+=1
				
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+':new information files. Change the dictionary\n')
				
				newfiles=findFile(init.stoixeiaDir)
				for name in newfiles:
					
					now=init.get_datetime()
					init.fp_log.write(now[0]+' '+now[1]+':delete information file\n')
					filename=init.stoixeiaDir+'/'+name+'.prc'
					os.remove(filename)
					
					print name
					print filename
					
					now=init.get_datetime()
					init.fp_log.write(now[0]+' '+now[1]+':update process file\n')
					
					filename=init.stoixeiaDir+'/'+name
					readStoixeia.update_dict(filename)
					
					
				
				time.sleep(5)
			
	
	init.fp_log.close()
	
	
