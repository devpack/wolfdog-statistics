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

		table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})
		table.setc(3, 0, "<i><u><b>NAME</b></u></i>")
		table.setc(3, 1, "<i><u><b>MOTHER</b></u></i>")
		table.setc(3, 2, "<i><u><b>FATHER</b></u></i>")
		table.setc(3, 3, "<i><u><b>GENDER</b></u></i>")
		table.setc(3, 4, "<i><u><b>BIRTHDAY</b></u></i>")
		table.setc(3, 5, "<i><u><b>HIP</b></u></i>")
		table.setc(3, 6, "<i><u><b>ED</b></u></i>")
		table.setc(3, 7, "<i><u><b>BONITATION</b></u></i>")
		table.setc(3, 8, "<i><u><b>COI5G</b></u></i>")
		table.setc(3, 9, "<i><u><b>AVK5G</b></u></i>")
		
		table.setc(3, 10, "<i><u><b>PRA</b></u></i>")
		table.setc(3, 11, "<i><u><b>INDEX_HEIGHT</b></u></i>")
		table.setc(3, 12, "<i><u><b>INDEX_FORMAT</b></u></i>")
		table.setc(3, 13, "<i><u><b>TRAINING</b></u></i>")
		table.setc(3, 14, "<i><u><b>OWNER</b></u></i>")
		
		table.setc(3, 15, "<i><u><b>BREEDER</b></u></i>")
		table.setc(3, 16, "<i><u><b>ORIGIN COUNTRY</b></u></i>")
		table.setc(3, 17, "<i><u><b>LIVING COUNTRY</b></u></i>")

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

				if IMAGE_DISPLAY:
					if os.path.isfile("pics/%s"%key.replace(".html", ".jpg")):
						table.setc(i+line, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
					else:
						table.setc(i+line, 0, "<a href=%s>%s</a>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
				else:
					table.setc(i+line, 0, "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, key.split(".")[0][1:], dump_dict[key]["NAME"]))

				table.setca(i+line, 0,{'bgcolor':"#333344"})

				parent_key = dump_dict[key]["MOTHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					table.setc(i+line, 1, "<h5><a href=%s/form.py?id=%s>%s</a></h5>"%(SERVER, dump_dict[key]["MOTHER"].split(".")[0][1:],dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?")))

				parent_key = dump_dict[key]["FATHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					table.setc(i+line, 2, "<h5><a href=%s/form.py?id=%s>%s</a></h5>"%(SERVER, dump_dict[key]["FATHER"].split(".")[0][1:],dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?")))

				table.setc(i+line, 3, dump_dict[key]["GENDER"].replace("data not available", "?"))

				if dump_dict[key]["BIRTHDAY"]!="data not available":
					table.setc(i+line, 4, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
				else:
					table.setc(i+line, 4, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

				table.setc(i+line, 5, dump_dict[key]["HIP"].replace("data not available", "?"))
				if dump_dict[key]["HIP"][:1]=="E":
					table.setca(i+line, 5,{'bgcolor':"#992222"})
				if dump_dict[key]["HIP"][:1]=="D":
					table.setca(i+line, 5,{'bgcolor':"#994455"})
				if dump_dict[key]["HIP"][:1]=="C":
					table.setca(i+line, 5,{'bgcolor':"#886622"})
				if dump_dict[key]["HIP"][:1]=="B":
					table.setca(i+line, 5,{'bgcolor':"#559922"})
				if dump_dict[key]["HIP"][:1]=="A":
					table.setca(i+line, 5,{'bgcolor':"#229922"})

				table.setc(i+line, 6, dump_dict[key]["ED"].replace("data not available", "?"))
				if dump_dict[key]["ED"] != "data not available":
					if dump_dict[key]["ED"] == "0-0":
						table.setca(i+line, 6,{'bgcolor':"#229922"})
					ed_val = dump_dict[key]["ED"].split("-")
					if "3" in ed_val:
						table.setca(i+line, 6,{'bgcolor':"#992222"})			
					if "2" in ed_val:
						table.setca(i+line, 6,{'bgcolor':"#994455"})
					if "1" in ed_val:
						table.setca(i+line, 6,{'bgcolor':"#886622"})

				table.setc(i+line, 7, dump_dict[key]["BONITATION"].replace("data not available", "?"))
				table.setc(i+line, 8, dump_dict[key]["COI5G"].replace("data not available", "?"))
				table.setc(i+line, 9, dump_dict[key]["AVK5G"].replace("data not available", "?"))

				table.setc(i+line, 10, dump_dict[key]["PRA"].replace("data not available", "?"))
				table.setc(i+line, 11, dump_dict[key]["INDEX_HEIGHT"].replace("data not available", "?"))
				table.setc(i+line, 12, dump_dict[key]["INDEX_FORMAT"].replace("data not available", "?"))
				table.setc(i+line, 13, dump_dict[key]["TRAINING"].replace("data not available", "?"))
				table.setc(i+line, 14, dump_dict[key]["OWNER"].replace("data not available", "?"))
				
				if dump_dict[key]["BREEDER"]!="data not available":
					table.setc(i+line, 15, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20" ), dump_dict[key]["BREEDER"].replace("data not available", "?")))
				else:
					table.setc(i+line, 15, dump_dict[key]["BREEDER"].replace("data not available", "?"))

				table.setc(i+line, 16, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
				table.setc(i+line, 17, dump_dict[key]["LIVING COUNTRY"].replace("data not available", "?"))

				# per contry stat
				key_contry = dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?")
				if country.has_key(key_contry):
					country[key_contry] += 1
				else:
					country[key_contry] = 1

				try:
					# coi stat
					coi_sum += float(dump_dict[key]["COI5G"][:-1])
					coifa_sum += float(dump_dict[key]["COIFA"][:-1])

					# avk stat
					avk5_sum += float(dump_dict[key]["AVK5G"][:-1])
					avk8_sum += float(dump_dict[key]["AVK8G"][:-1])
				except:
					pass

				i += 1

		# stat
		table.setc(0, 0, "<b>STATISTIC</b>")
		table.setca(0,0,{'bgcolor':"#AAAA11"})

		table.setc(1, 0, "%s: Total=%s"%(year, str(i)))

		#coi
		ss="<center>Average COI5G</center><br>"
		if i!=0:
			ss += str(coi_sum/i) + "%"
		table.setc(1, 2, ss)

		ss="<center>Average COI8G</center><br>"
		if i!=0:
			ss += str(coifa_sum/i) + "%"
		table.setc(1, 3, ss)

		#avk
		ss="<center>Average AVK5G</center><br>"
		if i!=0:
			ss += str(avk5_sum/i) + "%"
		table.setc(2, 2, ss)

		ss="<center>Average AVK8G</center><br>"
		if i!=0:
			ss += str(avk8_sum/i) + "%"
		table.setc(2, 3, ss)

		# country
		country_list = []
		for kkey in country:
			country_list.append((country[kkey], kkey))
		country_list.sort(reverse=True)
		ss=""
		for elem in country_list:
			ss += elem[1] + "=" + str(elem[0]) + "<br>"
		table.setc(2, 0, ss)

		#-------------------------------------------------------------------------------------

		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += table.return_html()
		resu += """</body></html>"""

		return resu	

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in find_id: %s"%e


try:
	form = cgi.FieldStorage()
	if form.has_key("year"):
		year = form["year"].value
		try:
			country = form["country"].value
		except:
			country = "all countries"
		s = find_birth(year, country)

	else:
		s = "You entered an empty expression"

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in find birth: %s"%e

