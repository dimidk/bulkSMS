#!/usr/bin/python
#-*- coding: utf-8-*-

import sys
import string
import os
import datetime
import init
import xlrd
import sendingSMS
from readStoixeia import StudentsStoixeia




""" διαβάζει τις απουσίες των μαθητών. ΑΜ, το όνομά τους.
Δημιουργεί ένα dictionary όπου αποθηκεύει τον ΑΜ,επώνυμο,όνομα και απουσίες όλων των μαθητών.
Τελειώνοντας την επεξεργασία των αρχείων τα μετονομάζει σε prc.Όταν εμφανιστεί νέο αρχείο xls σβήνει 
το παλιό prc, επεξεργάζεται το xls και το μετονομάζει. Στην επεξεργασία ελέγχει αν έχω μεταβολή 
των απουσιών των μαθητών απο το προηγούμενο αρχείο. Ο έλεγχος γίνεται στο dictionary."""


class StudentsAbsences():

	Studentsabsences=dict()
	
	def __init__(self,AM,Surname,Name,Absences):
		
		self.AM=int(AM)
		self.Surname=str(Surname)
		self.Name=str(Name)
		self.Absences=int(Absences)
		
		StudentsAbsences.Studentsabsences[self.AM]=[self.Surname,self.Name,self.Absences]


def read_AbsencesFile(filename):
	
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print "open file error"
		
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Students'' file '+ filename+ 'and add to dictionary\n')

	sheet=fp.sheet_by_index(0)
	print sheet.nrows
	for i in range(15,sheet.nrows,1):
		
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		am=sheet.row_values(i)[1]
		surname=sheet.row_values(i)[2]
		
		name=sheet.row_values(i)[3]
		absences=sheet.row_values(i)[5]
		
		s=StudentsAbsences(am,surname,name,absences)
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':add student  ' + str(s.AM) +' '+s.Surname+' '+s.Name+' '+str(s.Absences) +'\n')
		
	filename_prc=filename+'.prc'
	os.rename(filename,filename_prc)
	
	

def update_dict(filename):
	
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print "open file error"


	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read absences file'+filename+' and update dictionary\n')
	
	sheet=fp.sheet_by_index(0)
	print sheet.nrows
	for i in range(15,sheet.nrows,1):
		
		"""this is a solution for problem in converting unicode and ascii"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		am=sheet.row_values(i)[1]
		surname=sheet.row_values(i)[2]
		
		name=sheet.row_values(i)[3]
		absences=sheet.row_values(i)[5]
		
		if StudentsAbsences.Studentsabsences.has_key(int(am)):
			tmpStoixeia=StudentsAbsences.Studentsabsences.get(int(am))
			if tmpStoixeia[2]==int(absences):
				print "no absences changed"
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+': no absences changed\n')
				
				continue
			else:
				StudentsAbsences.Studentsabsences.pop(int(am))
				s=StudentsAbsences(am,surname,name,absences)
				
				
				tmpStoixeia=StudentsStoixeia.Studentstoixeia.get(s.AM)
				init.toSend=tmpStoixeia[2]
				print init.toSend
				
				init.studentName=s.Surname +' '+s.Name
				print init.studentName
								
				init.numberOfAbsences=str(s.Absences)
				print init.numberOfAbsences
				
				
				sendingSMS.sendSMS(i,init.toSend,init.fromSender,init.studentName,init.text,init.text1,init.numberOfAbsences)
				
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+':update student ' + str(s.AM) +' '+s.Surname+' '+s.Name+' '+str(s.Absences) +'\n')
			
	filename_prc=filename+'.prc'
	os.rename(filename,filename_prc)
		

def read_files():
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Students'' absences files\n')
	
	for root,dirs,filenames in os.walk(init.absencesDir,topdown=True):
		for name in filenames:
			filename=os.path.join(init.absencesDir,name)

			if 'xls' not in filename:
				continue
			read_AbsencesFile(filename)
			
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Complete Students'' absences dictionary\n')
	
	


