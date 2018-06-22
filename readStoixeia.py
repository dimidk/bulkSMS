#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import os
import datetime
import string
import init
import xlrd



""" διαβάζει τα στοιχεία των μαθητών. ΑΜ, το όνομά τους και το τηλέφωνο του κηδεμόνα.
Δημιουργεί ένα dictionary όπου αποθηκεύει τα στοιχεία όλων των μαθητών.Τελειώνοντας την επεξεργασία
των αρχείων τα μετονομάζει σε prc"""


class StudentsStoixeia():

	Studentstoixeia=dict()
	
	def __init__(self,AM,Surname,Name,PhoneNumber):
		
		self.AM=int(AM)
		self.Surname=str(Surname)
		self.Name=str(Name)
		
		self.PhoneNumber=str(PhoneNumber)
	
		StudentsStoixeia.Studentstoixeia[self.AM]=[self.Surname,self.Name,self.PhoneNumber]
	
def format(value):
    return "%.3f" % value	

def read_StoixeiaFile(filename):
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print "open file error"


	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Students'' file'+filename+' and add to dictionary\n')
	
	sheet=fp.sheet_by_index(0)

	for i in range(15,sheet.nrows,1):
		
		"""this is a solution for problem in converting unicode and ascii"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		am=sheet.row_values(i)[1]
		surname=sheet.row_values(i)[2]
		name=sheet.row_values(i)[4]
		phonenumber=sheet.row_values(i)[10]
		
		s=StudentsStoixeia(am,surname,name,phonenumber)
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':add student ' + str(s.AM) +' '+s.Surname+' '+s.Name+' '+s.PhoneNumber +'\n')
			
	filename_prc=filename+'.prc'
	os.rename(filename,filename_prc)
	

def update_dict(filename):
	
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print "open file error"


	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Students'' file'+filename+' and update dictionary\n')
	
	sheet=fp.sheet_by_index(0)
	print sheet.nrows
	for i in range(15,sheet.nrows,1):
		
		"""this is a solution for problem in converting unicode and ascii"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		am=sheet.row_values(i)[1]
		surname=sheet.row_values(i)[2]
		name=sheet.row_values(i)[4]
		phonenumber=sheet.row_values(i)[10]
		
		if StudentsStoixeia.Studentstoixeia.has_key(int(am)):
			tmpStoixeia=StudentsStoixeia.Studentstoixeia.get(int(am))
			
			StudentsStoixeia.Studentstoixeia.pop(int(am))
			s=StudentsStoixeia(am,surname,name,phonenumber)
			
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':update student ' + str(s.AM) +' '+s.Surname+' '+s.Name+' '+s.PhoneNumber +'\n')
			
	filename_prc=filename+'.prc'
	os.rename(filename,filename_prc)
	
	
	
	
def read_files():
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Students'' information files\n')
	
	for root,dirs,filenames in os.walk(init.stoixeiaDir,topdown=True):
		for name in filenames:
			filename=os.path.join(init.stoixeiaDir,name)
			
			if 'xls' not in filename:
				continue
			read_StoixeiaFile(filename)
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Complete Students'' information dictionary\n')
	
		

