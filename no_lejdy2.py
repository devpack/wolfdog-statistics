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

def no_lejdy(offspr):
	res = {}
	try:
		# ---init
		f = file("WDDB_utf8", 'rb')
		dump_dict = pck.load(f)
		f.close()

		f = file("NOLEJDYDB", 'rb')
		lejdy_dict = pck.load(f)
		f.close()

		table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})

		table.setc(3, 0, "<i><u><b>NAME</b></u></i>")
		table.setc(3, 1, "<i><u><b>GENDER</b></u></i>")
		table.setc(3, 2, "<i><u><b>MOTHER</b></u></i>")
		table.setc(3, 3, "<i><u><b>FATHER</b></u></i>")
		table.setc(3, 4, "<i><u><b>BONITATION</b></u></i>")
		table.setc(3, 5, "<i><u><b>HIP</b></u></i>")
		table.setc(3, 6, "<i><u><b>BIRTHDAY</b></u></i>")
		table.setc(3, 7, "<i><u><b>COI5G</b></u></i>")
		table.setc(3, 8, "<i><u><b>AVK5G</b></u></i>")
		table.setc(3, 9, "<i><u><b>BREEDER</b></u></i>")
		table.setc(3, 10, "<i><u><b>ORIGIN COUNTRY</b></u></i>")


		coi_sum = 0
		coifa_sum = 0

		avk5_sum = 0
		avk8_sum = 0

		i=0
		line=4
		country={}
		sorted_list=[]

		for key in lejdy_dict:
			sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

		sorted_list.sort(reverse=True)

		for elem in sorted_list:
			key = elem[1]

			cond = True

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
					table.setc(i+line, 0, "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, key.split(".")[0][1:], dump_dict[key]["NAME"]))

				table.setca(i+line, 0,{'bgcolor':"#333344"})

				table.setc(i+line, 1, dump_dict[key]["GENDER"].replace("data not available", "?"))

				parent_key = dump_dict[key]["MOTHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					#table.setc(i+line, 2, dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?"))
					table.setc(i+line, 2, "<h5><a href=%s/form.py?id=%s>%s</a></h5>"%(SERVER, parent_key.split(".")[0][1:],dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?")))

				parent_key = dump_dict[key]["FATHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					#table.setc(i+line, 3, dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?"))
					table.setc(i+line, 3, "<h5><a href=%s/form.py?id=%s>%s</a></h5>"%(SERVER, parent_key.split(".")[0][1:],dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?")))

				table.setc(i+line, 4, dump_dict[key]["BONITATION"].replace("data not available", "?"))
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
					table.setc(i+line, 6, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
				else:
					table.setc(i+line, 6, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

				table.setc(i+line, 7, dump_dict[key]["COI5G"].replace("data not available", "?"))
				table.setc(i+line, 8, dump_dict[key]["AVK5G"].replace("data not available", "?"))

				#table.setc(i+line, 7, dump_dict[key]["BREEDER"].replace("data not available", "?"))
				if dump_dict[key]["BREEDER"]!="data not available":
					table.setc(i+line, 9, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20"), dump_dict[key]["BREEDER"]))
				else:
					table.setc(i+line, 9, dump_dict[key]["BREEDER"].replace("data not available", "?"))

				table.setc(i+line, 10, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))

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


		# -- res string
		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += table.return_html()
		resu += """</body></html>"""

		return resu	

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in no_lejdy: %s"%e

#---------------------------------------------------------------------

try:
	form = cgi.FieldStorage()

	if form.has_key("offspring"):
		offspring = form["offspring"].value
		s = no_lejdy(offspring)
	else:
		s = no_lejdy(False)

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in no_lejdy: %s"%e


