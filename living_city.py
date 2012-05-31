#! /usr/bin/python

import cgi, time

import os, sys, urllib, time, pprint, re, datetime
import unicodedata

try:
	import cPickle as pck
except ImportError:
	import pickle as pck

import traceback as tb
import PyHtmlTable

SERVER = "http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin"
IMAGE_DISPLAY=False

def clean_it(txt):
	#f = open("/home/tony/Desktop/eeeeeeeeeee", "a+")
	#txt = u"h\xe9las"
	dectxt = unicodedata.normalize("NFD", txt)
	removechars = re.compile(u"[^\0-\x7f]")
	cleaned = removechars.sub("", dectxt)
	#f.write(cleaned)
	#print cleaned.encode("utf8")
	#print cleaned.encode("ascii")
	#print cleaned.encode("latin2")
	#f.close()
	return cleaned.lower()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Tool(object):
	def __init__(self, city):
		f = file("WDDB_utf8", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.city = city.lower()

		self.NO_ANCESTOR = ("d0.html", "d.html", "data not available")

		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1200','border':2})

		START=3

		self.table.setc(START, 0, "<i><u><b>NAME</b></u></i>")
		self.table.setc(START, 1, "<i><u><b>MOTHER</b></u></i>")
		self.table.setc(START, 2, "<i><u><b>FATHER</b></u></i>")
		self.table.setc(START, 3, "<i><u><b>GENDER</b></u></i>")
		self.table.setc(START, 4, "<i><u><b>BIRTHDAY</b></u></i>")
		self.table.setc(START, 5, "<i><u><b>COI5G</b></u></i>")
		self.table.setc(START, 6, "<i><u><b>HIP</b></u></i>")
		self.table.setc(START, 7, "<i><u><b>ED</b></u></i>")
		self.table.setc(START, 8, "<i><u><b>BONITATION</b></u></i>")
		self.table.setc(START, 9, "<i><u><b>BREEDER</b></u></i>")
		self.table.setc(START, 10, "<i><u><b>ORIGIN COUNTRY</b></u></i>")
		self.table.setc(START, 11, "<i><u><b>LIVING COUNTRY</b></u></i>")

		#print self.dump_dict["d976.html"]["NAME"].encode("hex")

	#-----------------------------------------------------------------------

	def go(self):

		try:
			p = re.compile(clean_it(self.city.decode("utf-8")))
		except:
			try:
				p = re.compile(clean_it(self.city.decode("latin1")))
			except:
				p = re.compile(self.city.lower())


		START=3

		result = []

		for key in self.dump_dict:

			if p.search( clean_it( self.dump_dict[key]["LIVING CITY"].decode("utf-8")) ):
				result.append((self.dump_dict[key]["BIRTHDAY"], key))

		result.sort()
		result.reverse()
		
		#print result

		city={}

		i=START
		j=0
		for el in result:

			key=el[1]

			if IMAGE_DISPLAY:
				if os.path.isfile("pics/%s"%key.replace(".html", ".jpg")):
					self.table.setc(1+i, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", key.replace(".html", ".jpg")),self.dump_dict[key]["NAME"]))
				else:
					self.table.setc(1+i, 0, "<a href=%s>%s</a>"%(os.path.join("pics", key.replace(".html", ".jpg")),self.dump_dict[key]["NAME"]))
			else:
				self.table.setc(i+1, 0, "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, key.split(".")[0][1:], self.dump_dict[key]["NAME"]))

			self.table.setca(i+1, 0,{'bgcolor':"#333344"})


			parent2_key = self.dump_dict[key]["MOTHER"]
			if parent2_key not in self.NO_ANCESTOR:
				self.table.setc(i+1, 1, "<h6><a href=%s/form.py?id=%s>%s</a></h6>"%(SERVER, parent2_key.split(".")[0][1:],self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))
			parent2_key = self.dump_dict[key]["FATHER"]

			if parent2_key not in self.NO_ANCESTOR:
				self.table.setc(i+1, 2, "<h6><a href=%s/form.py?id=%s>%s</a></h6>"%(SERVER, parent2_key.split(".")[0][1:],self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))


			self.table.setc(1+i, 3, self.dump_dict[key]["GENDER"].replace("data not available", "?"))

			#self.table.setc(1+i, 3, self.dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
			if self.dump_dict[key]["BIRTHDAY"]!="data not available":
				self.table.setc(i+1, 4, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict[key]["BIRTHDAY"],self.dump_dict[key]["BIRTHDAY"]))
			else:
				self.table.setc(i+1, 4, self.dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

			self.table.setc(1+i, 5, self.dump_dict[key]["COI5G"])

			self.table.setc(1+i, 6, self.dump_dict[key]["HIP"].replace("data not available", "?"))

			if self.dump_dict[key]["HIP"][:1]=="E":
				self.table.setca(i+1, 6,{'bgcolor':"#992222"})
			if self.dump_dict[key]["HIP"][:1]=="D":
				self.table.setca(i+1, 6,{'bgcolor':"#994455"})
			if self.dump_dict[key]["HIP"][:1]=="C":
				self.table.setca(i+1, 6,{'bgcolor':"#886622"})
			if self.dump_dict[key]["HIP"][:1]=="B":
				self.table.setca(i+1, 6,{'bgcolor':"#559922"})
			if self.dump_dict[key]["HIP"][:1]=="A":
				self.table.setca(i+1, 6,{'bgcolor':"#229922"})

			self.table.setc(1+i, 7, self.dump_dict[key]["ED"].replace("data not available", "?"))
			if self.dump_dict[key]["ED"] != "data not available":
				if self.dump_dict[key]["ED"] == "0-0":
					self.table.setca(1+i, 7,{'bgcolor':"#229922"})
				ed_val = self.dump_dict[key]["ED"].split("-")
				if "3" in ed_val:
					self.table.setca(1+i, 7,{'bgcolor':"#992222"})			
				if "2" in ed_val:
					self.table.setca(1+i, 7,{'bgcolor':"#994455"})
				if "1" in ed_val:
					self.table.setca(1+i, 7,{'bgcolor':"#886622"})


			self.table.setc(1+i, 8, self.dump_dict[key]["BONITATION"].replace("data not available", "?"))

			if self.dump_dict[key]["BREEDER"]!="data not available":
				self.table.setc(i+1, 9, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict[key]["BREEDER"].replace(" ", "%20" ), self.dump_dict[key]["BREEDER"]))
			else:
				self.table.setc(i+1, 9, self.dump_dict[key]["BREEDER"].replace("data not available", "?"))

			self.table.setc(1+i, 10, self.dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
			self.table.setc(1+i, 11, self.dump_dict[key]["LIVING COUNTRY"].replace("data not available", "?"))

			i+=1
			j+=1

		# stat
		self.table.setc(0, 0, "<b>STATISTIC</b>")
		self.table.setca(0,0,{'bgcolor':"#AAAA11"})
		self.table.setc(1, 0, "%s%s: TOTAL=%s"%(self.city[0].upper(), self.city[1:], str(j)))

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

def do_nb_offspring(city):
	try:
		T = Tool(city)
		T.go()
		return T.get_result()
	except Exception, e:
		print "Content-Type: text/html\n"
		print e


#-------------------------------------------------------------------------------

try:
	form = cgi.FieldStorage()
	if form.has_key("city"):
		city = form["city"].value
		s = do_nb_offspring(city)
	else:
		s = "You entered an empty string"



	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body TEXT="#FFFFFF" background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in living city: %s"%e









