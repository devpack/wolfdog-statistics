#! /usr/bin/python

import cgi, time

import re, sys, os
try:
	import cPickle as pck
except ImportError:
	import pickle as pck
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

def find_hd(hdstr, offspr):
	res = {}
	try:
		# ---init
		f = file("SWHDB", 'rb')
		dump_dict = pck.load(f)
		f.close()

		table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})

		table.setc(3, 0, "<i><u><b>NAME</b></u></i>")
		table.setc(3, 1, "<i><u><b>GENDER</b></u></i>")
		table.setc(3, 2, "<i><u><b>MOTHER</b></u></i>")
		table.setc(3, 3, "<i><u><b>FATHER</b></u></i>")
		table.setc(3, 4, "<i><u><b>PRA</b></u></i>")
		table.setc(3, 5, "<i><u><b>HIP</b></u></i>")
		table.setc(3, 6, "<i><u><b>BIRTHDAY</b></u></i>")
		table.setc(3, 7, "<i><u><b>DWARF GENE</b></u></i>")
		table.setc(3, 8, "<i><u><b>ORIGIN COUNTRY</b></u></i>")
		table.setc(3, 9, "<i><u><b>COLOR</b></u></i>")
		table.setc(3, 10, "<i><u><b>DECEASED</b></u></i>")

		i=0
		line=4
		country={}
		sorted_list=[]

		for key in dump_dict:
			birth = dump_dict[key]["BIRTHDAY"].split("/")
			sorted_list.append( ((birth[2],birth[1],birth[0]), key))

		sorted_list.sort()

		for elem in sorted_list:
			key = elem[1]

			cond = re.search(hdstr.lower(), dump_dict[key]["HIP"].lower().replace("data not available", ""))

			# offspring
			if offspr == "True":
				cond = cond and dump_dict[key].has_key("OFFSPRING")

			# or cond on boni code
			if cond:

				if IMAGE_DISPLAY:
					if os.path.isfile("pics/%s"%key.replace(".html", ".jpg")):
						table.setc(i+line, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
					else:
						table.setc(i+line, 0, "<a href=%s>%s</a>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
				else:
					table.setc(i+line, 0, "<a href=%s/saarloos.py?id=%s>%s</a>"%(SERVER, key, dump_dict[key]["NAME"]))

				table.setca(i+line, 0,{'bgcolor':"#333344"})

				table.setc(i+line, 1, dump_dict[key]["GENDER"].replace("data not available", "?"))

				parent_key = dump_dict[key]["MOTHER"]
				if parent_key not in ("d0.html", "d.html"):
					#table.setc(i+line, 2, dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?"))
					table.setc(i+line, 2, "<h5><a href=%s/saarloos.py?id=%s>%s</a></h5>"%(SERVER, parent_key,dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?")))

				parent_key = dump_dict[key]["FATHER"]
				if parent_key not in ("d0.html", "d.html"):
					#table.setc(i+line, 3, dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?"))
					table.setc(i+line, 3, "<h5><a href=%s/saarloos.py?id=%s>%s</a></h5>"%(SERVER, parent_key,dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?")))

				table.setc(i+line, 4, dump_dict[key]["PRA"].replace("data not available", "?"))
				if dump_dict[key]["PRA"] != "data not available":
					if is_sick( dump_dict[key]["PRA"] ):
						table.setca(i+line, 4,{'bgcolor':"#994455"})
					else:
						table.setca(i+line, 4,{'bgcolor':"#229922"})

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

				#table.setc(i+line, 6, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
				if dump_dict[key]["BIRTHDAY"]!="data not available":
					table.setc(i+line, 6, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
				else:
					table.setc(i+line, 6, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))


				table.setc(i+line, 7, dump_dict[key]["DWARF"].replace("data not available", "?"))
				if dump_dict[key]["DWARF"] != "data not available":
					if is_sick( dump_dict[key]["DWARF"] ):
						table.setca(i+line, 7,{'bgcolor':"#994455"})
					else:
						table.setca(i+line, 7,{'bgcolor':"#229922"})

				table.setc(i+line, 8, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
				table.setc(i+line, 9, dump_dict[key]["COAT_COLOR"].replace("data not available", "?"))
				table.setc(i+line, 10, dump_dict[key]["DECEASED"].replace("data not available", "?"))

				# per contry stat
				key_contry = dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?")
				if country.has_key(key_contry):
					country[key_contry] += 1
				else:
					country[key_contry] = 1

				i += 1

		# stat
		table.setc(0, 0, "<b>STATISTIC</b>")
		table.setca(0,0,{'bgcolor':"#AAAA11"})
		table.setc(1, 0, "TOTAL=%s"%str(i))

		country_list = []
		for kkey in country:
			country_list.append((country[kkey], kkey))
		country_list.sort(reverse=True)
		ss=""
		for elem in country_list:
			ss += elem[1] + "=" + str(elem[0]) + "<br>"
		table.setc(2, 0, ss)
		

		# -- res string
		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += table.return_html()
		resu += """</body></html>"""

		return resu	

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in find_hd: %s"%e

#---------------------------------------------------------------------

try:
	form = cgi.FieldStorage()
	if form.has_key("hd"):
		hd = form["hd"].value
		if form.has_key("offspring"):
			offspring = form["offspring"].value
			s = find_hd(hd, offspring)
		else:
			s = find_hd(hd, False)
	else:
		s = "You entered an empty expression"

	print "Content-Type: text/html\n"
	print """<html><HEAD><TITLE>swh stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in find_hd: %s"%e


