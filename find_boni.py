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

def find_boni(expr, offspr, the_country):
	res = {}
	try:
		# ---init
		f = file("WDDB_utf8", 'rb')
		dump_dict = pck.load(f)
		f.close()

		table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})

		table.setc(0, 0, "<i><u><b>NAME</b></u></i>")
		table.setc(0, 1, "<i><u><b>ID</b></u></i>")
		table.setc(0, 2, "<i><u><b>GENDER</b></u></i>")
		table.setc(0, 3, "<i><u><b>BONITATION</b></u></i>")
		table.setc(0, 4, "<i><u><b>HIP</b></u></i>")
		table.setc(0, 5, "<i><u><b>BIRTHDAY</b></u></i>")
		table.setc(0, 6, "<i><u><b>BREEDER</b></u></i>")
		table.setc(0, 7, "<i><u><b>ORIGIN COUNTRY</b></u></i>")

		# --- regular expression
		if expr[:6] == "regex:":
			rgex = expr.split("regex:")[1]

			i=0
			line=1
			sorted_list=[]


			for key in dump_dict:
				if the_country.lower() =="all countries":
					sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))
				else:
					if the_country.lower() == dump_dict[key]["ORIGIN COUNTRY"].lower():
						sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

			sorted_list.sort(reverse=True)

			for elem in sorted_list:
				key = elem[1]
				p = re.compile(rgex.lower())
				cond = p.search(dump_dict[key]["BONITATION"].lower())

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

					table.setc(i+line, 1, "ID=%s"%key[1:-5])
					table.setc(i+line, 2, dump_dict[key]["GENDER"].replace("data not available", "?"))
					table.setc(i+line, 3, dump_dict[key]["BONITATION"].replace("data not available", "?"))
					table.setc(i+line, 4, dump_dict[key]["HIP"].replace("data not available", "?"))
					if dump_dict[key]["HIP"][:1]=="E":
						table.setca(i+line, 4,{'bgcolor':"#992222"})
					if dump_dict[key]["HIP"][:1]=="D":
						table.setca(i+line, 4,{'bgcolor':"#994455"})
					if dump_dict[key]["HIP"][:1]=="C":
						table.setca(i+line, 4,{'bgcolor':"#886622"})
					if dump_dict[key]["HIP"][:1]=="B":
						table.setca(i+line, 4,{'bgcolor':"#559922"})
					if dump_dict[key]["HIP"][:1]=="A":
						table.setca(i+line, 4,{'bgcolor':"#229922"})

					#table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
					if dump_dict[key]["BIRTHDAY"]!="data not available":
						table.setc(i+line, 5, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
					else:
						table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

					#table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))
					if dump_dict[key]["BREEDER"]!="data not available":
						table.setc(i+line, 6, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20" ), dump_dict[key]["BREEDER"].replace("data not available", "?")))
					else:
						table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))

					table.setc(i+line, 7, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
					i += 1
		
		# --- or
		pos_or = expr.find("or")
		if pos_or >=0:
			or_expr_list = expr.split("or")

			if or_expr_list:
				#print "or_expr_list", or_expr_list
				i=0
				line=1
				sorted_list=[]


				for key in dump_dict:
					if the_country.lower() =="all countries":
						sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))
					else:
						if the_country.lower() == dump_dict[key]["ORIGIN COUNTRY"].lower():
							sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

				sorted_list.sort(reverse=True)

				for elem in sorted_list:
					key = elem[1]

					cond = False
					for rex in or_expr_list:
						cond = cond or re.search(rex.lower().replace(" ", ""), dump_dict[key]["BONITATION"].lower())

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

						table.setc(i+line, 1, "ID=%s"%key[1:-5])
						table.setc(i+line, 2, dump_dict[key]["GENDER"].replace("data not available", "?"))
						table.setc(i+line, 3, dump_dict[key]["BONITATION"].replace("data not available", "?"))
						table.setc(i+line, 4, dump_dict[key]["HIP"].replace("data not available", "?"))
						if dump_dict[key]["HIP"][:1]=="E":
							table.setca(i+line, 4,{'bgcolor':"#992222"})
						if dump_dict[key]["HIP"][:1]=="D":
							table.setca(i+line, 4,{'bgcolor':"#994455"})
						if dump_dict[key]["HIP"][:1]=="C":
							table.setca(i+line, 4,{'bgcolor':"#886622"})
						if dump_dict[key]["HIP"][:1]=="B":
							table.setca(i+line, 4,{'bgcolor':"#559922"})
						if dump_dict[key]["HIP"][:1]=="A":
							table.setca(i+line, 4,{'bgcolor':"#229922"})

						#table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
						if dump_dict[key]["BIRTHDAY"]!="data not available":
							table.setc(i+line, 5, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
						else:
							table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

						#table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))
						if dump_dict[key]["BREEDER"]!="data not available":
							table.setc(i+line, 6, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20" ), dump_dict[key]["BREEDER"].replace("data not available", "?")))
						else:
							table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))
						table.setc(i+line, 7, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
						i += 1

		# --- and
		pos_and = expr.find("and")
		if pos_and >=0:
			and_expr_list = expr.split("and")

			if and_expr_list:
				#print "and_expr_list", and_expr_list
				i=0
				line=1
				sorted_list=[]

				for key in dump_dict:
					if the_country.lower() =="all countries":
						sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))
					else:
						if the_country.lower() == dump_dict[key]["ORIGIN COUNTRY"].lower():
							sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

				sorted_list.sort(reverse=True)

				for elem in sorted_list:
					key = elem[1]

					cond = True
					for rex in and_expr_list:
						cond = cond and re.search(rex.lower().replace(" ", ""), dump_dict[key]["BONITATION"].lower())
						
					# offspring
					if offspr == "True":
						cond = cond and dump_dict[key].has_key("OFFSPRING")

					# and cond on boni code
					if cond:		
						if IMAGE_DISPLAY:
							if os.path.isfile("pics/%s"%key.replace(".html", ".jpg")):
								table.setc(i+line, 0, "<u><a href=%s>%s</a></u>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
							else:
								table.setc(i+line, 0, "<a href=%s>%s</a>"%(os.path.join("pics", key.replace(".html", ".jpg")),dump_dict[key]["NAME"]))
						else:
							table.setc(i+line, 0, "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, key.split(".")[0][1:], dump_dict[key]["NAME"]))

						table.setca(i+line, 0,{'bgcolor':"#333344"})

						table.setc(i+line, 1, "ID=%s"%key[1:-5])
						table.setc(i+line, 2, dump_dict[key]["GENDER"].replace("data not available", "?"))
						table.setc(i+line, 3, dump_dict[key]["BONITATION"].replace("data not available", "?"))
						table.setc(i+line, 4, dump_dict[key]["HIP"].replace("data not available", "?"))
						if dump_dict[key]["HIP"][:1]=="E":
							table.setca(i+line, 4,{'bgcolor':"#992222"})
						if dump_dict[key]["HIP"][:1]=="D":
							table.setca(i+line, 4,{'bgcolor':"#994455"})
						if dump_dict[key]["HIP"][:1]=="C":
							table.setca(i+line, 4,{'bgcolor':"#886622"})
						if dump_dict[key]["HIP"][:1]=="B":
							table.setca(i+line, 4,{'bgcolor':"#559922"})
						if dump_dict[key]["HIP"][:1]=="A":
							table.setca(i+line, 4,{'bgcolor':"#229922"})

						#table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
						if dump_dict[key]["BIRTHDAY"]!="data not available":
							table.setc(i+line, 5, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
						else:
							table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

						#table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))
						if dump_dict[key]["BREEDER"]!="data not available":
							table.setc(i+line, 6, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20" ), dump_dict[key]["BREEDER"].replace("data not available", "?")))
						else:
							table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))
						table.setc(i+line, 7, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
						i += 1

		# --- ni or ni and
		pos_or = expr.find("or")
		pos_and = expr.find("and")
		if pos_or<0 and pos_and<0:
			i=0
			line=1
			sorted_list=[]

			for key in dump_dict:
				if the_country.lower() =="all countries":
					sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))
				else:
					if the_country.lower() == dump_dict[key]["ORIGIN COUNTRY"].lower():
						sorted_list.append( (dump_dict[key]["BIRTHDAY"].replace("data not available", "?"), key))

			sorted_list.sort(reverse=True)

			for elem in sorted_list:
				key = elem[1]

				cond = re.search(expr.lower(), dump_dict[key]["BONITATION"].lower())

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

					table.setc(i+line, 1, "ID=%s"%key[1:-5])
					table.setc(i+line, 2, dump_dict[key]["GENDER"].replace("data not available", "?"))
					table.setc(i+line, 3, dump_dict[key]["BONITATION"].replace("data not available", "?"))

					table.setc(i+line, 4, dump_dict[key]["HIP"].replace("data not available", "?"))
					if dump_dict[key]["HIP"][:1]=="E":
						table.setca(i+line, 4,{'bgcolor':"#992222"})
					if dump_dict[key]["HIP"][:1]=="D":
						table.setca(i+line, 4,{'bgcolor':"#994455"})
					if dump_dict[key]["HIP"][:1]=="C":
						table.setca(i+line, 4,{'bgcolor':"#886622"})
					if dump_dict[key]["HIP"][:1]=="B":
						table.setca(i+line, 4,{'bgcolor':"#559922"})
					if dump_dict[key]["HIP"][:1]=="A":
						table.setca(i+line, 4,{'bgcolor':"#229922"})

					#table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))
					if dump_dict[key]["BIRTHDAY"]!="data not available":
						table.setc(i+line, 5, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]))
					else:
						table.setc(i+line, 5, dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))

					#table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))

					if dump_dict[key]["BREEDER"]!="data not available":
						table.setc(i+line, 6, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20" ), dump_dict[key]["BREEDER"].replace("data not available", "?")))
					else:
						table.setc(i+line, 6, dump_dict[key]["BREEDER"].replace("data not available", "?"))

					table.setc(i+line, 7, dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))
					i += 1



		# -- res string
		resu = ""
		resu += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		resu += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		resu += table.return_html()
		resu += """</body></html>"""

		return resu	

	except Exception, e:
		print "Content-Type: text/html\n"
		print "Error in find_boni: %s"%e

#---------------------------------------------------------------------

try:
	form = cgi.FieldStorage()
	if form.has_key("expr"):
		expr = form["expr"].value
		if form.has_key("offspring"):
			offspring = form["offspring"].value
			country = form["country"].value
			s = find_boni(expr, offspring, country)

		else:
			country = form["country"].value
			s = find_boni(expr, False, country)
	else:
		s = "You entered an empty expression"

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in find_boni: %s"%e


