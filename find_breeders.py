#! /usr/bin/python

import cgi, time

import re, sys, os
import unicodedata
import traceback as tb

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

def sani(name):
	return name.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").replace("*", "").replace("?", "").replace("-", "").replace("&", "").replace(".", "").replace("|", "").replace(" ", "")

def go(breeder_name):
	breeder_name_svg = breeder_name
	breeder_name = sani(breeder_name.replace("%20", " "))

	#breeder_name = breeder_name.split(" ")[0]
	#print breeder_name

	try:
		try:
			p = re.compile(clean_it(breeder_name.decode("utf-8")))
		except:
			try:
				p = re.compile(clean_it(breeder_name.decode("latin1")))
			except:
				p = re.compile(breeder_name.lower())

		#p = re.compile(clean_it(breeder_name.decode("utf-8")))
		f = file("WDDB_utf8", 'rb')
		dump_dict = pck.load(f)
		f.close()

		table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})
		table.setc(4, 0, "<i><u><b>NAME</b></u></i>")
		table.setc(4, 1, "<i><u><b>ID</b></u></i>")
		table.setc(4, 2, "<i><u><b>GENDER</b></u></i>")
		table.setc(4, 3, "<i><u><b>MOTHER</b></u></i>")
		table.setc(4, 4, "<i><u><b>FATHER</b></u></i>")
		table.setc(4, 5, "<i><u><b>BIRTHDAY</b></u></i>")
		table.setc(4, 6, "<i><u><b>HIP</b></u></i>")
		table.setc(4, 7, "<i><u><b>ED</b></u></i>")
		table.setc(4, 8, "<i><u><b>BONITATION</b></u></i>")
		table.setc(4, 9, "<i><u><b>COI5G</b></u></i>")
		table.setc(4, 10, "<i><u><b>AVK5G</b></u></i>")
		table.setc(4, 11, "<i><u><b>BREEDER</b></u></i>")
		table.setc(4, 12, "<i><u><b>ORIGIN COUNTRY</b></u></i>")
		table.setc(4, 13, "<i><u><b>LIVING COUNTRY</b></u></i>")

		i=0
		line=5
		birth_dict = {}
		hd_dict = {}
		ed_dict = {}
		coi_sum = 0
		coifa_sum = 0
		avk5_sum = 0
		avk8_sum = 0

		sorted_list=[]

		country = {}

		for key in dump_dict:
			if p.search( clean_it( sani(dump_dict[key]["BREEDER"]).decode("utf-8")) ):
				sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

		# error, try shorter name search
		if not sorted_list:
			breeder_name = breeder_name_svg
			breeder_name = breeder_name.split(" ")[0]
			breeder_name = sani(breeder_name.replace("%20", " "))

			try:
				p = re.compile(clean_it(breeder_name.decode("utf-8")))
			except:
				try:
					p = re.compile(clean_it(breeder_name.decode("latin1")))
				except:
					p = re.compile(breeder_name.lower())

			for key in dump_dict:
				if p.search( clean_it( sani(dump_dict[key]["BREEDER"]).decode("utf-8")) ):
					sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

		sorted_list.sort(reverse=True)

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

				table.setc(i+line, 1, key[1:-5])
				table.setc(i+line, 2, dump_dict[key]["GENDER"].replace("data not available", "?"))

				parent_key = dump_dict[key]["MOTHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					#table.setc(i+line, 3, dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?"))
					table.setc(i+line, 3, "<h5><a href=%s/form.py?id=%s>%s</a></h5>"%(SERVER, dump_dict[key]["MOTHER"].split(".")[0][1:],dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?")))

				parent_key = dump_dict[key]["FATHER"].replace("data not available", "?")
				if parent_key not in ("d0.html", "d.html"):
					table.setc(i+line, 4, dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?"))
					table.setc(i+line, 4, "<h5><a href=%s/form.py?id=%s>%s</a></h5>"%(SERVER, dump_dict[key]["FATHER"].split(".")[0][1:],dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?")))

				if dump_dict[key]["BIRTHDAY"]!="data not available":
					table.setc(i+line, 5, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
				else:
					table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

				table.setc(i+line, 6, dump_dict[key]["HIP"].replace("data not available", "?"))
				if dump_dict[key]["HIP"][:1]=="E":
					table.setca(i+line, 6,{'bgcolor':"#992222"})
				if dump_dict[key]["HIP"][:1]=="D":
					table.setca(i+line, 6,{'bgcolor':"#994455"})
				if dump_dict[key]["HIP"][:1]=="C":
					table.setca(i+line, 6,{'bgcolor':"#886622"})
				if dump_dict[key]["HIP"][:1]=="B":
					table.setca(i+line, 6,{'bgcolor':"#559922"})
				if dump_dict[key]["HIP"][:1]=="A":
					table.setca(i+line, 6,{'bgcolor':"#229922"})

				table.setc(i+line, 7, dump_dict[key]["ED"].replace("data not available", "?"))
				if dump_dict[key]["ED"] != "data not available":
					if dump_dict[key]["ED"] == "0-0":
						table.setca(i+line, 7,{'bgcolor':"#229922"})
					ed_val = dump_dict[key]["ED"].split("-")
					if "3" in ed_val:
						table.setca(i+line, 7,{'bgcolor':"#992222"})			
					if "2" in ed_val:
						table.setca(i+line, 7,{'bgcolor':"#994455"})
					if "1" in ed_val:
						table.setca(i+line, 7,{'bgcolor':"#886622"})

				table.setc(i+line, 8, dump_dict[key]["BONITATION"].replace("data not available", "?"))
				table.setc(i+line, 9, dump_dict[key]["COI5G"].replace("data not available", "?"))
				table.setc(i+line, 10, dump_dict[key]["AVK5G"].replace("data not available", "?"))

				#table.setc(i+line, 10, dump_dict[key]["BREEDER"].replace("data not available", "?"))
				
				table.setc(i+line, 11, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20"), dump_dict[key]["BREEDER"].replace("data not available", "?")))

				table.setc(i+line, 12, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
				table.setc(i+line, 13, dump_dict[key]["LIVING COUNTRY"].replace("data not available", "?"))

				# per birth stat
				key_birth = dump_dict[key]["BIRTHDAY"].replace("data not available", "?")
				if key_birth != "?":
					key_birth = key_birth.split(".")[0]

				if birth_dict.has_key(key_birth):
					birth_dict[key_birth] += 1
				else:
					birth_dict[key_birth] = 1

				try:
					# coi stat
					coi_sum += float(dump_dict[key]["COI5G"][:-1])
					coifa_sum += float(dump_dict[key]["COIFA"][:-1])

					# avk stat
					avk5_sum += float(dump_dict[key]["AVK5G"][:-1])
					avk8_sum += float(dump_dict[key]["AVK8G"][:-1])
				except:
					pass

				# hd stat
				key_hd = dump_dict[key]["HIP"].replace("data not available", "?")
				if hd_dict.has_key(key_hd[:1]):
					hd_dict[key_hd[:1]] += 1
				else:
					hd_dict[key_hd[:1]] = 1

				# ed stat
				key_ed = dump_dict[key]["ED"].replace("data not available", "?")
				val = "?"
				if key_ed != "?":
					if key_ed == "0-0":
						val = "0"
					ed_val = key_ed.split("-")
					if "3" in ed_val:
						val = "3"
					if "2" in ed_val:
						val = "2"
					if "1" in ed_val:
						val = "1"

				if ed_dict.has_key(val):
					ed_dict[val] += 1
				else:
					ed_dict[val] = 1

				# per contry stat
				key_contry = dump_dict[key]["LIVING COUNTRY"].replace("data not available", "?")
				if country.has_key(key_contry):
					country[key_contry] += 1
				else:
					country[key_contry] = 1

				i += 1
 

		# name
		table.setc(0, 0, "<b>%s</b>"%breeder_name_svg)
		table.setca(0,0,{'bgcolor':"#333377"})

		# stat
		table.setc(1, 0, "<b>STATISTIC</b>")
		table.setca(1,0,{'bgcolor':"#AAAA11"})

		country_list = []
		for kkey in country:
			country_list.append((country[kkey], kkey))
		country_list.sort(reverse=True)
		ss=""
		for elem in country_list:
			ss += elem[1] + "=" + str(elem[0]) + "<br>"

		table.setc(2, 0, "<i>TOTAL Dogs</i>=%s<br><br><u>Dogs living in:</u><br><br>%s"%(str(i), ss))

		# hd
		hd_list = []
		for kkey in hd_dict:
			hd_list.append((kkey, hd_dict[kkey]))
		hd_list.sort()

		ss="<center>HD</center><br>"
		for elem in hd_list:
			ss += elem[0] + "=" + str(elem[1]) + "<br>"
		table.setc(2, 2, ss) # hd

		#coi
		ss="<center>Average COI5G</center><br>"
		if i!=0:
			ss += str(coi_sum/i) + "%"
		table.setc(2, 3, ss)

		ss="<center>Average COI8G</center><br>"
		if i!=0:
			ss += str(coifa_sum/i) + "%"
		table.setc(2, 4, ss)

		#avk
		ss="<center>Average AVK5G</center><br>"
		if i!=0:
			ss += str(avk5_sum/i) + "%"
		table.setc(3, 3, ss)

		ss="<center>Average AVK8G</center><br>"
		if i!=0:
			ss += str(avk8_sum/i) + "%"
		table.setc(3, 4, ss)

		# ed
		ed_list = []
		for kkey in ed_dict:
			ed_list.append((kkey, ed_dict[kkey]))
		ed_list.sort()

		ss="<center>ED</center><br>"
		for elem in ed_list:
			ss += elem[0] + "=" + str(elem[1]) + "<br>"
		table.setc(3, 2, ss) # ed

		# birth
		birth_list = []
		for kkey in birth_dict:
			birth_list.append((kkey, birth_dict[kkey]))
		birth_list.sort(reverse=True)
		
		ss=""
		for elem in birth_list:
			ss += elem[0] + "=" + str(elem[1]) + "<br>"
		table.setc(3, 0, ss)
		

		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += table.return_html()
		resu += """</body></html>"""

		return resu	

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in find_breeder: %s"%e
		print exc_detail()


def exc_detail():
	exc = tb.extract_tb(sys.exc_info()[2])[0]
	exc_mess = "Exception type='%s', from file='%s', line number='%s', function='%s', code line='%s'"%(sys.exc_info()[1], exc[0], exc[1], exc[2], exc[3])
	return exc_mess


try:
	form = cgi.FieldStorage()
	if form.has_key("name"):
		name = form["name"].value
		#s = go(name.split(" ")[0])
		s = go(name)
	else:
		s = "You entered an empty name"

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body TEXT="#FFFFFF" background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in find breeders: %s"%e

