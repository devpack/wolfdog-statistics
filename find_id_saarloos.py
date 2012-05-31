#! /usr/bin/python

import cgi

import re, sys, os
import unicodedata
import time

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


def find_id(dog_name):

	try:
		try:
			p = re.compile(clean_it(dog_name.decode("utf-8")))
		except:
			try:
				p = re.compile(clean_it(dog_name.decode("latin1")))
			except:
				p = re.compile(dog_name.lower())

		#p = re.compile(clean_it(dog_name.decode("utf-8")))
		f = file("SWHDB", 'rb')
		dump_dict = pck.load(f)
		f.close()

		table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})
		table.setc(0, 0, "<i><u><b>NAME</b></u></i>")
		table.setc(0, 1, "<i><u><b>ID</b></u></i>")
		table.setc(0, 2, "<i><u><b>GENDER</b></u></i>")
		table.setc(0, 3, "<i><u><b>MOTHER</b></u></i>")
		table.setc(0, 4, "<i><u><b>FATHER</b></u></i>")
		table.setc(0, 5, "<i><u><b>BIRTHDAY</b></u></i>")
		table.setc(0, 6, "<i><u><b>DECEASED</b></u></i>")
		table.setc(0, 7, "<i><u><b>HIP</b></u></i>")
		table.setc(0, 8, "<i><u><b>ED</b></u></i>")
		table.setc(0, 9, "<i><u><b>PRA</b></u></i>")
		table.setc(0, 10, "<i><u><b>COI5G</b></u></i>")
		table.setc(0, 11, "<i><u><b>DWARF GENE</b></u></i>")
		table.setc(0, 12, "<i><u><b>ORIGIN COUNTRY</b></u></i>")
		table.setc(0, 13, "<i><u><b>REG NUM</b></u></i>")
		table.setc(0, 14, "<i><u><b>COLOR</b></u></i>")
		i=0
		line=1

		sorted_list=[]
		for key in dump_dict:
			if p.search( clean_it( dump_dict[key]["NAME"].decode("utf-8")) ):
				birth = dump_dict[key]["BIRTHDAY"].split("/")
				sorted_list.append( ((birth[2],birth[1],birth[0]), key))
				#sorted_list.append( (dump_dict[key]["BIRTHDAY"], key))

		sorted_list.sort()

		for elem in sorted_list:
				key = elem[1]

				if IMAGE_DISPLAY:
					if os.path.isfile("pics/%s"%key.replace(".html", ".jpg")):
						table.setc(i+line, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
					else:
						table.setc(i+line, 0, "<a href=%s>%s</a>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
				else:
					table.setc(i+line, 0, "<a href=%s/saarloos.py?id=%s>%s</a>"%(SERVER, key, dump_dict[key]["NAME"]))

				table.setca(i+line, 0,{'bgcolor':"#333344"})

				table.setc(i+line, 1, key)
				table.setc(i+line, 2, dump_dict[key]["GENDER"].replace("data not available", "?"))

				parent_key = dump_dict[key]["MOTHER"]
				if parent_key not in ("data not available"):
					table.setc(i+line, 3, "<h5><a href=%s/saarloos.py?id=%s>%s</a></h5>"%(SERVER, dump_dict[key]["MOTHER"],dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?")))
				else:
					table.setc(i+line, 3, "?")

				parent_key = dump_dict[key]["FATHER"]
				if parent_key not in ("data not available"):
					table.setc(i+line, 4, "<h5><a href=%s/saarloos.py?id=%s>%s</a></h5>"%(SERVER, dump_dict[key]["FATHER"],dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?")))
				else:
					table.setc(i+line, 4, "?")

				if dump_dict[key]["BIRTHDAY"]!="data not available":
					table.setc(i+line, 5, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
				else:
					table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

				
				table.setc(i+line, 6, dump_dict[key]["DECEASED"].replace("data not available", "?"))
				

				table.setc(i+line, 7, dump_dict[key]["HIP"].replace("data not available", "?"))
				if dump_dict[key]["HIP"][:1]=="E":
					table.setca(i+line, 7,{'bgcolor':"#992222"})
				if dump_dict[key]["HIP"][:1]=="D":
					table.setca(i+line, 7,{'bgcolor':"#994455"})
				if dump_dict[key]["HIP"][:1]=="C":
					table.setca(i+line, 7,{'bgcolor':"#886622"})
				if dump_dict[key]["HIP"][:1]=="B":
					table.setca(i+line, 7,{'bgcolor':"#559922"})
				if dump_dict[key]["HIP"][:1]=="A":
					table.setca(i+line, 7,{'bgcolor':"#229922"})

				table.setc(i+line, 8, dump_dict[key]["ED"].replace("data not available", "?"))
				if dump_dict[key]["ED"] != "data not available":
					if dump_dict[key]["ED"] == "0-0":
						table.setca(i+1, 8,{'bgcolor':"#229922"})
					ed_val = dump_dict[key]["ED"].split("-")
					if "3" in ed_val:
						table.setca(i+1, 8,{'bgcolor':"#992222"})			
					if "2" in ed_val:
						table.setca(i+1, 8,{'bgcolor':"#994455"})
					if "1" in ed_val:
						table.setca(i+1, 8,{'bgcolor':"#886622"})

				table.setc(i+line, 9, dump_dict[key]["PRA"].replace("data not available", "?"))
				if dump_dict[key]["PRA"] != "data not available":
					if is_sick( dump_dict[key]["PRA"] ):
						table.setca(i+line, 9,{'bgcolor':"#994455"})
					else:
						table.setca(i+line, 9,{'bgcolor':"#229922"})

				table.setc(i+line, 10, dump_dict[key]["COI5G"].replace("data not available", "?"))
				
				table.setc(i+line, 11, dump_dict[key]["DWARF"].replace("data not available", "?"))
				if dump_dict[key]["DWARF"] != "data not available":
					if is_sick( dump_dict[key]["DWARF"] ):
						table.setca(i+line, 11,{'bgcolor':"#994455"})
					else:
						table.setca(i+line, 11,{'bgcolor':"#229922"})

				table.setc(i+line, 12, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
				table.setc(i+line, 13, dump_dict[key]["REG_NUM"].replace("data not available", "?"))
				table.setc(i+line, 14, dump_dict[key]["COAT_COLOR"].replace("data not available", "?"))
				i += 1

		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += table.return_html()
		resu += """</body></html>"""

		return resu

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in find_id: %s"%e




#---------------------------------------------------------------------

try:
	form = cgi.FieldStorage()
	if form.has_key("dog_name"):
		dog_name = form["dog_name"].value

		s = find_id(dog_name)
	else:
		s = "You entered an empty name"

	print "Content-Type: text/html\n"
	print """<html><HEAD><TITLE>swh stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in find_id: %s"%e























