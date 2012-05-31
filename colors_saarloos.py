#! /usr/bin/python

import cgi, time

import os, sys, urllib, time, pprint, re, datetime

try:
	import cPickle as pck
except ImportError:
	import pickle as pck

import traceback as tb
import PyHtmlTable

SERVER = "http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin"
IMAGE_DISPLAY=False

def is_sick(s):
	b = False

	sl = s.lower()	
	
	pos = sl.find("not")
	if pos >= 0:
		b = True

	pos = sl.find("posit")
	if pos >= 0:
		b = True

	pos = sl.find("carrier")
	if pos >= 0:
		b = True

	pos = sl.find("aff") #Affect AFFLICT
	if pos >= 0:
		b = True

	return b

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Tool(object):
	def __init__(self, color):
		f = file("SWHDB", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.COLOR = color

		self.NO_ANCESTOR = ("data not available")

		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1200','border':2})
		self.table.setc(0, 0, "<i><u><b>NAME</b></u></i>")
		self.table.setc(0, 1, "<i><u><b>MOTHER</b></u></i>")
		self.table.setc(0, 2, "<i><u><b>FATHER</b></u></i>")
		self.table.setc(0, 3, "<i><u><b>GENDER</b></u></i>")
		self.table.setc(0, 4, "<i><u><b>BIRTHDAY</b></u></i>")
		self.table.setc(0, 5, "<i><u><b>HIP</b></u></i>")
		self.table.setc(0, 6, "<i><u><b>PRA</b></u></i>")
		self.table.setc(0, 7, "<i><u><b>DWARF GENE</b></u></i>")
		self.table.setc(0, 8, "<i><u><b>COLOR</b></u></i>")
		self.table.setc(0, 9, "<i><u><b>ORIGIN COUNTRY</b></u></i>")

		#print self.dump_dict["d976.html"]["NAME"].encode("hex")

	#-----------------------------------------------------------------------

	def go(self):
		result = []

		for key in self.dump_dict:
			
			if self.COLOR=="White":
				self.COLOR = "white"
			if self.COLOR=="Wolf-gray":
				self.COLOR = "gray"
			if self.COLOR=="Forest-Brown":
				self.COLOR = "brown"

			pos = self.dump_dict[key]["COAT_COLOR"].lower().find(self.COLOR)

			if pos >= 0:
				
				# birth check
				if self.dump_dict[key]["BIRTHDAY"] != "data not available":
					dt = self.dump_dict[key]["BIRTHDAY"].split("/")
					try:
						result.append((dt[2], key))
					except:
						result.append((1900, key))
				else:
					result.append((1900, key))

		result.sort()
		result.reverse()
		
		#print result

		i=0
		for el in result:

			if IMAGE_DISPLAY:
				if os.path.isfile("pics/%s"%el[1].replace(".html", ".jpg")):
					self.table.setc(1+i, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", el[1].replace(".html", ".jpg")),self.dump_dict[el[1]]["NAME"]))
				else:
					self.table.setc(1+i, 0, "<a href=%s>%s</a>"%(os.path.join("pics", el[1].replace(".html", ".jpg")),self.dump_dict[el[1]]["NAME"]))
			else:
				self.table.setc(i+1, 0, "<a href=%s/saarloos.py?id=%s>%s</a>"%(SERVER, el[1], self.dump_dict[el[1]]["NAME"]))

			self.table.setca(i+1, 0,{'bgcolor':"#333344"})

			parent2_key = self.dump_dict[el[1]]["MOTHER"]
			if parent2_key not in self.NO_ANCESTOR:
				self.table.setc(i+1, 1, "<h6><a href=%s/saarloos.py?id=%s>%s</a></h6>"%(SERVER, parent2_key,self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))

			parent2_key = self.dump_dict[el[1]]["FATHER"]
			if parent2_key not in self.NO_ANCESTOR:
				self.table.setc(i+1, 2, "<h6><a href=%s/saarloos.py?id=%s>%s</a></h6>"%(SERVER, parent2_key,self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))

			self.table.setc(1+i, 3, self.dump_dict[el[1]]["GENDER"].replace("data not available", "?"))

			#self.table.setc(1+i, 3, self.dump_dict[el[1]]["BIRTHDAY"].replace("data not available", "?"))
			if self.dump_dict[el[1]]["BIRTHDAY"]!="data not available":
				self.table.setc(i+1, 4, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[el[1]]["BIRTHDAY"],self.dump_dict[el[1]]["BIRTHDAY"]))
			else:
				self.table.setc(i+1, 4, self.dump_dict[el[1]]["BIRTHDAY"].replace("data not available", "?"))

			self.table.setc(1+i, 5, self.dump_dict[el[1]]["HIP"].replace("data not available", "?"))
			key=el[1]
			if self.dump_dict[key]["HIP"][:1]=="E":
				self.table.setca(i+1, 5,{'bgcolor':"#992222"})
			if self.dump_dict[key]["HIP"][:1]=="D":
				self.table.setca(i+1, 5,{'bgcolor':"#994455"})
			if self.dump_dict[key]["HIP"][:1]=="C":
				self.table.setca(i+1, 5,{'bgcolor':"#886622"})
			if self.dump_dict[key]["HIP"][:1]=="B":
				self.table.setca(i+1, 5,{'bgcolor':"#559922"})
			if self.dump_dict[key]["HIP"][:1]=="A":
				self.table.setca(i+1, 5,{'bgcolor':"#229922"})

			self.table.setc(1+i, 6, self.dump_dict[el[1]]["PRA"].replace("data not available", "?"))
			if self.dump_dict[el[1]]["PRA"] != "data not available":
				if is_sick( self.dump_dict[el[1]]["PRA"] ):
					self.table.setca(1+i, 6,{'bgcolor':"#994455"})
				else:
					self.table.setca(1+i, 6,{'bgcolor':"#229922"})

			self.table.setc(i+1, 7, self.dump_dict[el[1]]["DWARF"].replace("data not available", "?"))
			if self.dump_dict[el[1]]["DWARF"] != "data not available":
				if is_sick( self.dump_dict[el[1]]["DWARF"] ):
					self.table.setca(1+i, 7,{'bgcolor':"#994455"})
				else:
					self.table.setca(1+i, 7,{'bgcolor':"#229922"})

			self.table.setc(1+i, 8, self.dump_dict[el[1]]["COAT_COLOR"].replace("data not available", "?"))
			self.table.setc(1+i, 9, self.dump_dict[el[1]]["ORIGIN COUNTRY"].replace("data not available", "?"))

			i+=1

	#-----------------------------------------------------------------------

	def get_result(self):
		res = ""
		res += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		res += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		res += self.table.return_html()
		res += """</body></html>"""
		return res

#-------------------------------------------------------------------------------

def exc_detail():
	exc = tb.extract_tb(sys.exc_info()[2])[0]
	exc_mess = "Exception type='%s', from file='%s', line number='%s', function='%s', code line='%s'"%(sys.exc_info()[1], exc[0], exc[1], exc[2], exc[3])
	return exc_mess

def do_nb_offspring(color):
	try:
		T = Tool(color)
		T.go()
		return T.get_result()
	except Exception, e:
		print "Content-Type: text/html\n"
		print e


#-------------------------------------------------------------------------------

try:
	form = cgi.FieldStorage()
	if form.has_key("color"):
		color = form["color"].value
		s = do_nb_offspring(color)
	else:
		s = "You entered an empty field"

	print "Content-Type: text/html\n"
	print """<html><HEAD><TITLE>swh stat</TITLE></HEAD>"""
	print """<body TEXT="#FFFFFF" background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in nb_offspring: %s"%e









