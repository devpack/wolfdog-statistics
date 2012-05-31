#! /usr/bin/python

import cgi, time

import re, sys, os
import unicodedata

try:
	import cPickle as pck
except ImportError:
	import pickle as pck
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

def find_birth(year, the_country):

	year = year.split(".")[0]
	#print year

	try:
		try:
			p = re.compile(clean_it(year.decode("utf-8")))
		except:
			try:
				p = re.compile(clean_it(year.decode("latin1")))
			except:
				p = re.compile(year.lower())

		#p = re.compile(clean_it(year.decode("utf-8")))
		f = file("WDDB_utf8", 'rb')
		dump_dict = pck.load(f)
		f.close()

		o = ""
		o += "NAME" + "\t"
		o += "MOTHER" + "\t"
		o += "FATHER" + "\t"
		o += "GENDER" + "\t"
		o += "BIRTHDAY" + "\t"
		o += "HIP" + "\t"
		o += "ED" + "\t"
		o += "BONITATION" + "\t"
		o += "COI5G" + "\t"
		o += "AVK5G" + "\t"
		o += "PRA" + "\t"
		o += "INDEX_HEIGHT" + "\t"
		o += "INDEX_FORMAT" + "\t"
		o += "TRAINING" + "\t"
		o += "OWNER" + "\t"
		o += "BREEDER" + "\t"
		o += "ORIGIN COUNTRY" + "\t"
		o += "LIVING COUNTRY" + "\t"
		o += "\n\n"

		i=0
		line=4
		country={}

		coi_sum = 0
		coifa_sum = 0

		avk5_sum = 0
		avk8_sum = 0

		sorted_list=[]


		for key in dump_dict:
			if the_country.lower() =="all countries":
				if p.search( clean_it( dump_dict[key]["BIRTHDAY"].decode("utf-8")) ):
					sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))
			else:
				if the_country.lower() == dump_dict[key]["ORIGIN COUNTRY"].lower():
					if p.search( clean_it( dump_dict[key]["BIRTHDAY"].decode("utf-8")) ):
						sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

		sorted_list.sort()


		for elem in sorted_list:
				key = elem[1]

				o += dump_dict[key]["NAME"] + "\t"

				parent_key = dump_dict[key]["MOTHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					o += dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?") + "\t"
				else:
					o += "?"  + "\t"
				parent_key = dump_dict[key]["FATHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					o += dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?") + "\t"
				else:
					o += "?"  + "\t"

				o += dump_dict[key]["GENDER"].replace("data not available", "?")  + "\t"

				if dump_dict[key]["BIRTHDAY"]!="data not available":
					o += dump_dict[key]["BIRTHDAY"]  + "\t"
				else:
					o += dump_dict[key]["BIRTHDAY"].replace("data not available", "?")  + "\t"

				o += dump_dict[key]["HIP"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["ED"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["BONITATION"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["COI5G"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["AVK5G"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["PRA"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["INDEX_HEIGHT"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["INDEX_FORMAT"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["TRAINING"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["OWNER"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["BREEDER"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?")   + "\t"
				o += dump_dict[key]["LIVING COUNTRY"].replace("data not available", "?")   + "\t"

				# per contry stat
				key_contry = dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?")
				if country.has_key(key_contry):
					country[key_contry] += 1
				else:
					country[key_contry] = 1

				# coi stat
				coi_sum += float(dump_dict[key]["COI5G"][:-1])
				coifa_sum += float(dump_dict[key]["COIFA"][:-1])

				# avk stat
				avk5_sum += float(dump_dict[key]["AVK5G"][:-1])
				avk8_sum += float(dump_dict[key]["AVK8G"][:-1])

				o += "\n"

				i += 1

		z = ""
		# stat
		z += "STATISTIC\t"
		z+= "%s: Total=%s\t"%(year, str(i))

		#coi
		ss="Average COI5G\t"
		if i!=0:
			ss += str(coi_sum/i) + "%"
		z += ss +"\t"
		
		ss="Average COI8G\t"
		if i!=0:
			ss += str(coifa_sum/i) + "%"
		z += ss +"\t"

		#avk
		ss="Average AVK5G\t"
		if i!=0:
			ss += str(avk5_sum/i) + "%"
		z += ss +"\t"

		ss="Average AVK8G\t"
		if i!=0:
			ss += str(avk8_sum/i) + "%"
		z += ss +"\t"

		# country
		country_list = []
		for kkey in country:
			country_list.append((country[kkey], kkey))
		country_list.sort(reverse=True)
		ss=""
		for elem in country_list:
			ss += elem[1] + "=" + str(elem[0]) + "\t"
		z += ss +"\t"
		z+="\n\n"
		#-------------------------------------------------------------------------------------

		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += """</body></html>"""

		return o, z

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in find_id: %s"%e



try:
	form = cgi.FieldStorage()
	if form.has_key("year"):
		year = form["year"].value
		country = form["country"].value
		o,z = find_birth(year, country)

	else:
		s = "You entered an empty expression"

	print "Content-Type: text\n"
	#print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	#print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s%s"""%(z, o)
	#print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in find birth: %s"%e

