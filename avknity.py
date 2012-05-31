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

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Tool(object):
	def __init__(self, limit, from_year):
		f = file("WDDB_utf8", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.LIMIT = int(limit)
		self.FROM_YEAR = datetime.date( int(from_year), int(1), int(1) )

		self.NO_ANCESTOR = ("d0.html", "d.html")

		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1200','border':2})

		START=3

		self.table.setc(START, 0, "<i><u><b>NAME</b></u></i>")
		self.table.setc(START, 1, "<i><u><b>AVK5G</b></u></i>")
		self.table.setc(START, 2, "<i><u><b>COI5G</b></u></i>")
		self.table.setc(START, 3, "<i><u><b>GENDER</b></u></i>")
		self.table.setc(START, 4, "<i><u><b>BIRTHDAY</b></u></i>")
		self.table.setc(START, 5, "<i><u><b>HIP</b></u></i>")
		self.table.setc(START, 6, "<i><u><b>BONITATION</b></u></i>")
		self.table.setc(START, 7, "<i><u><b>BREEDER</b></u></i>")
		self.table.setc(START, 8, "<i><u><b>ORIGIN COUNTRY</b></u></i>")

		#print self.dump_dict["d976.html"]["NAME"].encode("hex")

	#-----------------------------------------------------------------------

	def go(self):

		START=3

		result = []

		for key in self.dump_dict:

			# birth check
			if self.dump_dict[key]["BIRTHDAY"] != "data not available":
				dt = self.dump_dict[key]["BIRTHDAY"].split(".")
				try:
					if len(dt)==3:
						birth = datetime.date( int(dt[0]), int(dt[1]), int(dt[2]) )
					if len(dt)==2:
						birth = datetime.date( int(dt[0]), int(dt[1]), int(1) )
					if len(dt)==1:
						birth = datetime.date( int(dt[0]), int(1), int(1) )
					if birth > self.FROM_YEAR:
						result.append((float(self.dump_dict[key]["AVK5G"][:-1]), key))
				except:
					pass

			# no birth available, print anyway
			else:
				result.append((float(self.dump_dict[key]["AVK5G"][:-1]), key))

		result.sort()
		#result.reverse()
		
		#print result

		country={}

		i=START
		j=0
		for el in result[:self.LIMIT]:

			key=el[1]

			if IMAGE_DISPLAY:
				if os.path.isfile("pics/%s"%key.replace(".html", ".jpg")):
					self.table.setc(1+i, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", key.replace(".html", ".jpg")),self.dump_dict[key]["NAME"]))
				else:
					self.table.setc(1+i, 0, "<a href=%s>%s</a>"%(os.path.join("pics", key.replace(".html", ".jpg")),self.dump_dict[key]["NAME"]))
			else:
				self.table.setc(i+1, 0, "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, key.split(".")[0][1:], self.dump_dict[key]["NAME"]))

			self.table.setca(i+1, 0,{'bgcolor':"#333344"})

			self.table.setc(1+i, 1, self.dump_dict[key]["AVK5G"])
			self.table.setc(1+i, 2, self.dump_dict[key]["COI5G"])

			self.table.setc(1+i, 3, self.dump_dict[key]["GENDER"].replace("data not available", "?"))

			#self.table.setc(1+i, 3, self.dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
			if self.dump_dict[key]["BIRTHDAY"]!="data not available":
				self.table.setc(i+1, 4, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict[key]["BIRTHDAY"],self.dump_dict[key]["BIRTHDAY"]))
			else:
				self.table.setc(i+1, 4, self.dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

			self.table.setc(1+i, 5, self.dump_dict[key]["HIP"].replace("data not available", "?"))

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

			self.table.setc(1+i, 6, self.dump_dict[key]["BONITATION"].replace("data not available", "?"))

			if self.dump_dict[key]["BREEDER"]!="data not available":
				self.table.setc(i+1, 7, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict[key]["BREEDER"].replace(" ", "%20" ), self.dump_dict[key]["BREEDER"]))
			else:
				self.table.setc(i+1, 7, self.dump_dict[key]["BREEDER"].replace("data not available", "?"))

			self.table.setc(1+i, 8, self.dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))

			i+=1
			j+=1

			# per contry stat
			key_contry = self.dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?")
			if country.has_key(key_contry):
				country[key_contry] += 1
			else:
				country[key_contry] = 1


		# stat
		self.table.setc(0, 0, "<b>STATISTIC</b>")
		self.table.setca(0,0,{'bgcolor':"#AAAA11"})
		self.table.setc(1, 0, "Display first %s born after %s"%(str(j), self.FROM_YEAR))

		country_list = []
		for kkey in country:
			country_list.append((country[kkey], kkey))
		country_list.sort(reverse=True)
		ss=""
		for elem in country_list:
			ss += elem[1] + "=" + str(elem[0]) + "<br>"
		self.table.setc(2, 0, ss)

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

def do_nb_offspring(limit, from_year):
	try:
		T = Tool(limit, from_year)
		T.go()
		return T.get_result()
	except Exception, e:
		print "Content-Type: text/html\n"
		print e


#-------------------------------------------------------------------------------

try:
	form = cgi.FieldStorage()
	if form.has_key("limit"):
		limit = form["limit"].value
	else:
		limit = 100

	if form.has_key("from_year"):
		from_year = form["from_year"].value
	else:
		from_year = 1900

	s = do_nb_offspring(limit, from_year)

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body TEXT="#FFFFFF" background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in nb_offspring: %s"%e









