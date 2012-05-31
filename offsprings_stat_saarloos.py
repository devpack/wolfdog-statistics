#! /usr/bin/python

import cgi

import os, sys, urllib, time, pprint, re
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
	def __init__(self, dog_id, depth):
		self.DEEP_STOP = int(depth)
		self.DOG_ID = dog_id

		f = file("SWHDB", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.NO_ANCESTOR = ("data not available")
		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})

	#-----------------------------------------------------------------------

	def go(self):
		self.offspring_dict = {0: self.DOG_ID}

		self.nb_desc_custom_done = []
		self.nb_desc_custom = 0
		self.tree_parse(self.DOG_ID, 0)
		#print self.offspring_dict

		self.calcul_stat()
		self.htmlprint_stat()

	#-----------------------------------------------------------------------

	def tree_parse(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			if self.dump_dict[node_key].has_key("OFFSPRING"):
				
				for child_key in self.dump_dict[node_key]["OFFSPRING"]:
					
					if child_key not in self.nb_desc_custom_done:
						
						if self.offspring_dict.has_key(deep+1):
							self.offspring_dict[deep+1].append( child_key )
						else:
							self.offspring_dict[deep+1] = [child_key]

						self.nb_desc_custom += 1
						self.nb_desc_custom_done.append(child_key)
						self.tree_parse(child_key, deep+1)


		except Exception, e:
			print "Error tree_parse: %s"%e
			print exc_detail()


	#-----------------------------------------------------------------------

	def calcul_stat(self):
		try:
			# --- HD
			self.HD_dict={}
			for i in range(self.DEEP_STOP):
				if self.offspring_dict.has_key(i+1):
					for ancetre_list in self.offspring_dict[i+1]:
						if self.dump_dict[ancetre_list]["HIP"] != "data not available":
							if self.HD_dict.has_key(self.dump_dict[ancetre_list]["HIP"][:1]):
								self.HD_dict[self.dump_dict[ancetre_list]["HIP"][:1]] += 1
							else:
								self.HD_dict[self.dump_dict[ancetre_list]["HIP"][:1]] = 1
						else:
							if self.HD_dict.has_key("?"):
								self.HD_dict["?"] += 1
							else:
								self.HD_dict["?"] = 1

			#print self.HD_dict



			# --- nb offspring 1G
			if self.dump_dict[self.DOG_ID].has_key("OFFSPRING"):
				self.nb_desc_onegen = len(self.dump_dict[self.DOG_ID]["OFFSPRING"])
			else:
				self.nb_desc_onegen = 0

			# nb offspring all G
			self.MAX_DEEP = 99
			self.nb_desc_allgen_done = []
			self.nb_desc_allgen = 0
			self.rec_nb_offspring(self.DOG_ID, 0)

			self.custom_nb_desc_done = []
			self.custom_nb_desc = 0
			self.custom_rec_nb_offspring(self.DOG_ID, 0)

			#print self.nb_desc_allgen

		except Exception, e:
			print "Error calcul_stat: %s"%e
			print exc_detail()

	#-----------------------------------------------------------------------

	def rec_nb_offspring(self, node_key, deep):
		try:
			if deep == self.MAX_DEEP:
				return

			if self.dump_dict[node_key].has_key("OFFSPRING"):
				for child_key in self.dump_dict[node_key]["OFFSPRING"]:
					if child_key not in self.nb_desc_allgen_done:
						self.nb_desc_allgen += 1
						self.nb_desc_allgen_done.append(child_key)
						self.rec_nb_offspring(child_key, deep+1)

		except Exception, e:
			print "Error rec_nb_offspring: %s"%e
			print exc_detail()

	#-----------------------------------------------------------------------

	def custom_rec_nb_offspring(self, node_key, deep):
		try:
			if deep == self.DEEP_STOP:
				return

			if self.dump_dict[node_key].has_key("OFFSPRING"):
				for child_key in self.dump_dict[node_key]["OFFSPRING"]:
					if child_key not in self.custom_nb_desc_done:
						self.custom_nb_desc += 1
						self.custom_nb_desc_done.append(child_key)
						self.custom_rec_nb_offspring(child_key, deep+1)

		except Exception, e:
			print "Error custom_rec_nb_offspring: %s"%e
			print exc_detail()


	#-----------------------------------------------------------------------

	def htmlprint_stat(self):
		try:
			# dog name
			self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID) ; self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Color</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>PRA</u></i>") ; self.table.setc(0, 8, "<i><u>DWARF GENE</u></i>") ; self.table.setc(0, 9, "<i><u>Country</u></i>") ; self.table.setc(0, 10, "<i><u>Birthday</u></i>"); self.table.setc(0, 11, "<i><u>Deceased</u></i>")
	    		self.table.setca(0,0,{'bgcolor':"#AA0000"})

			self.table.setc(1, 1, "<b><a href=%s/saarloos.py?id=%s>%s</a></b>"%(SERVER, self.DOG_ID, self.dump_dict[self.DOG_ID]["NAME"]))

			self.table.setc(1, 2, self.dump_dict[self.DOG_ID]["GENDER"].replace("data not available", "?"))
			self.table.setc(1, 3, self.dump_dict[self.DOG_ID]["COAT_COLOR"].replace("data not available", "?"))
			self.table.setc(1, 4, self.dump_dict[self.DOG_ID]["INDEX_HEIGHT"].replace("data not available", "?"))
			self.table.setc(1, 5, self.dump_dict[self.DOG_ID]["INDEX_FORMAT"].replace("data not available", "?"))

			self.table.setc(1, 6, self.dump_dict[self.DOG_ID]["HIP"].replace("data not available", "?"))
			if self.dump_dict[self.DOG_ID]["HIP"] != "data not available":
				if self.dump_dict[self.DOG_ID]["HIP"][:1]=="E":
					self.table.setca(1, 6,{'bgcolor':"#992222"})
				if self.dump_dict[self.DOG_ID]["HIP"][:1]=="D":
					self.table.setca(1, 6,{'bgcolor':"#994455"})
				if self.dump_dict[self.DOG_ID]["HIP"][:1]=="C":
					self.table.setca(1, 6,{'bgcolor':"#886622"})
				if self.dump_dict[self.DOG_ID]["HIP"][:1]=="B":
					self.table.setca(1, 6,{'bgcolor':"#559922"})
				if self.dump_dict[self.DOG_ID]["HIP"][:1]=="A":
					self.table.setca(1, 6,{'bgcolor':"#229922"})

			self.table.setc(1, 7, self.dump_dict[self.DOG_ID]["PRA"].replace("data not available", "?"))
			if self.dump_dict[self.DOG_ID]["PRA"] != "data not available":
				if is_sick( self.dump_dict[self.DOG_ID]["PRA"] ):
					self.table.setca(1, 7,{'bgcolor':"#994455"})
				else:
					self.table.setca(1, 7,{'bgcolor':"#229922"})

			self.table.setc(1, 8, self.dump_dict[self.DOG_ID]["DWARF"].replace("data not available", "?"))
			if self.dump_dict[self.DOG_ID]["DWARF"] != "data not available":
				if is_sick( self.dump_dict[self.DOG_ID]["DWARF"] ):
					self.table.setca(1, 8,{'bgcolor':"#994455"})
				else:
					self.table.setca(1, 8,{'bgcolor':"#229922"})

			self.table.setc(1, 9, self.dump_dict[self.DOG_ID]["ORIGIN COUNTRY"].replace("data not available", "?"))

			#self.table.setc(1, 10, self.dump_dict[self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))
			if self.dump_dict[self.DOG_ID]["BIRTHDAY"]!="data not available":
				self.table.setc(1, 10, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[self.DOG_ID]["BIRTHDAY"],self.dump_dict[self.DOG_ID]["BIRTHDAY"]))
			else:
				self.table.setc(1, 10, self.dump_dict[self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))

			self.table.setc(1, 11, self.dump_dict[self.DOG_ID]["DECEASED"].replace("data not available", "?"))


			# stat
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"}) ; self.table.setc(3, 1, "for depth=%s"%self.DEEP_STOP)
			self.table.setc(4, 0, "HD") ;  self.table.setc(4, 1, self.HD_dict)

			self.table.setc(7, 0, "Offspring") ;  self.table.setc(7, 1, "1Gen=%s | %sGen=%s | allGen=%s"%(self.nb_desc_onegen, self.DEEP_STOP, self.custom_nb_desc,self.nb_desc_allgen))		


			# tree
			START = 9
			self.table.setc(START, 0, "<b>FAMILY TREE</b>") ; self.table.setca(START,0,{'bgcolor':"#0000AA"})
			self.table.setc(START+1, 0, "<i><u>Depth</u></i>") ; self.table.setc(START+1, 1, "<i><u>Name</u></i>")
			
			self.table.setc(START+1, 2, "<i><u>Mother</u></i>")
			self.table.setc(START+1, 3, "<i><u>Father</u></i>")

			self.table.setc(START+1, 4, "<i><u>Gender</u></i>") ; self.table.setc(START+1, 5, "<i><u>Color</u></i>") ; self.table.setc(START+1, 6, "<i><u>Idx H</u></i>") ; self.table.setc(START+1, 7, "<i><u>Idx F</u></i>") ; self.table.setc(START+1, 8, "<i><u>HD</u></i>") ; self.table.setc(START+1, 9, "<i><u>PRA</u></i>") ; self.table.setc(START+1, 10, "<i><u>DWARF GENE</u></i>") ; self.table.setc(START+1, 11, "<i><u>Country</u></i>") ; self.table.setc(START+1, 12, "<i><u>Birthday</u></i>"); self.table.setc(START+1, 13, "<i><u>Deceased</u></i>")

			line=START+2
			for i in range(self.DEEP_STOP):
				if self.offspring_dict.has_key(i+1):

					# sort offspring
					sorted_off={}
					for ancetre_list in self.offspring_dict[i+1]:
						if sorted_off.has_key(self.dump_dict[ancetre_list]["BIRTHDAY"]):
							sorted_off[self.dump_dict[ancetre_list]["BIRTHDAY"]].append(ancetre_list)
						else:
							sorted_off[self.dump_dict[ancetre_list]["BIRTHDAY"]] = [ancetre_list]

					# sort offspring
					sorted_keys = sorted_off.keys()
					sorted_keys.sort()
					sorted_list=[]
					for key in sorted_keys:
						sorted_list += sorted_off[key]

					# display info 
					for ancetre_list in sorted_list:
						self.table.setc(i+line, 0, i+1)

						if IMAGE_DISPLAY:
							# name
							if os.path.isfile("pics/%s"%ancetre_list.replace(".html", ".jpg")):
								self.table.setc(i+line, 1, "<u><a href=%s>%s</a></u>"%("pics/%s"%ancetre_list.replace(".html", ".jpg"),self.dump_dict[ancetre_list]["NAME"]))
							else:
								self.table.setc(i+line, 1, "<a href=%s>%s</a>"%("pics/%s"%ancetre_list.replace(".html", ".jpg"),self.dump_dict[ancetre_list]["NAME"]))
						else:
							self.table.setc(i+line, 1, "<a href=%s/saarloos.py?id=%s>%s</a>"%(SERVER, ancetre_list,self.dump_dict[ancetre_list]["NAME"]))
						abool=True
						if self.dump_dict[ancetre_list]["NAME"] in ("FLEUR WOLVIN", "FLEUR II WOLVIN"):
							self.table.setca(i+line, 1,{'bgcolor':"#223366"})
							abool=False

						if re.search("F1", self.dump_dict[ancetre_list]["NAME"]) or re.search("F2", self.dump_dict[ancetre_list]["NAME"]) or re.search("F3", self.dump_dict[ancetre_list]["NAME"]) or re.search("F4", self.dump_dict[ancetre_list]["NAME"]) or re.search("F5", self.dump_dict[ancetre_list]["NAME"]) or re.search("F6", self.dump_dict[ancetre_list]["NAME"]):
							self.table.setca(i+line, 1,{'bgcolor':"#227766"})
							abool=False

						if abool:
							self.table.setca(i+line, 1,{'bgcolor':"#222233"})

						parent2_key = self.dump_dict[ancetre_list]["MOTHER"]
						if parent2_key not in self.NO_ANCESTOR:
							#self.table.setc(i+line, 2, self.dump_dict[parent2_key]["NAME"])
							self.table.setc(i+line, 2, "<h6><a href=%s/saarloos.py?id=%s>%s</a></h6>"%(SERVER, parent2_key,self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))
						parent2_key = self.dump_dict[ancetre_list]["FATHER"]
						if parent2_key not in self.NO_ANCESTOR:
							#self.table.setc(i+line, 3, self.dump_dict[parent2_key]["NAME"])
							self.table.setc(i+line, 3, "<h6><a href=%s/saarloos.py?id=%s>%s</a></h6>"%(SERVER, parent2_key,self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))
						self.table.setc(i+line, 4, self.dump_dict[ancetre_list]["GENDER"].replace("data not available", "?"))
						self.table.setc(i+line, 5, self.dump_dict[ancetre_list]["COAT_COLOR"].replace("data not available", "?"))
						self.table.setc(i+line, 6, self.dump_dict[ancetre_list]["INDEX_HEIGHT"].replace("data not available", "?"))
						self.table.setc(i+line, 7, self.dump_dict[ancetre_list]["INDEX_FORMAT"].replace("data not available", "?"))

						# hip
						self.table.setc(i+line, 8, self.dump_dict[ancetre_list]["HIP"].replace("data not available", "?"))
						if self.dump_dict[ancetre_list]["HIP"][:1]=="E":
							self.table.setca(i+line, 8,{'bgcolor':"#992222"})
						if self.dump_dict[ancetre_list]["HIP"][:1]=="D":
							self.table.setca(i+line, 8,{'bgcolor':"#994455"})
						if self.dump_dict[ancetre_list]["HIP"][:1]=="C":
							self.table.setca(i+line, 8,{'bgcolor':"#886622"})
						if self.dump_dict[ancetre_list]["HIP"][:1]=="B":
							self.table.setca(i+line, 8,{'bgcolor':"#559922"})
						if self.dump_dict[ancetre_list]["HIP"][:1]=="A":
							self.table.setca(i+line, 8,{'bgcolor':"#229922"})

						self.table.setc(i+line, 9, self.dump_dict[ancetre_list]["PRA"].replace("data not available", "?"))
						if self.dump_dict[ancetre_list]["PRA"] != "data not available":
							if is_sick( self.dump_dict[ancetre_list]["PRA"] ):
								self.table.setca(i+line, 9,{'bgcolor':"#994455"})
							else:
								self.table.setca(i+line, 9,{'bgcolor':"#229922"})

						self.table.setc(i+line, 10, self.dump_dict[ancetre_list]["DWARF"].replace("data not available", "?"))
						if self.dump_dict[ancetre_list]["DWARF"] != "data not available":
							if is_sick( self.dump_dict[ancetre_list]["DWARF"] ):
								self.table.setca(i+line, 10,{'bgcolor':"#994455"})
							else:
								self.table.setca(i+line, 10,{'bgcolor':"#229922"})

						self.table.setc(i+line, 11, self.dump_dict[ancetre_list]["ORIGIN COUNTRY"].replace("data not available", "?"))

						#self.table.setc(i+line, 12, self.dump_dict[ancetre_list]["BIRTHDAY"].replace("data not available", "?"))
						if self.dump_dict[ancetre_list]["BIRTHDAY"]!="data not available":
							self.table.setc(i+line, 12, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[ancetre_list]["BIRTHDAY"],self.dump_dict[ancetre_list]["BIRTHDAY"]))
						else:
							self.table.setc(i+line, 12, self.dump_dict[ancetre_list]["BIRTHDAY"].replace("data not available", "?"))

						self.table.setc(i+line, 13, self.dump_dict[ancetre_list]["DECEASED"].replace("data not available", "?"))


						line+=1



			#self.write_html()

		except Exception, e:
			print "Content-Type: text/html\n"
			print exc_detail()

	#-----------------------------------------------------------------------

	def get_result(self):
		res = ""
		res += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		res += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		res += self.table.return_html()
		res += """</body></html>"""
		return res

	#-----------------------------------------------------------------------

	def write_html(self):
		# write
		f = open("%s.html"%self.DOG_ID, "wb")
		f.write("""<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">""")
		f.write("""<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>""")
		f.write(self.table.return_html())
		f.write("""</body></html>""")
		f.close()

#-------------------------------------------------------------------------------

def exc_detail():
	exc = tb.extract_tb(sys.exc_info()[2])[0]
	exc_mess = "Exception type='%s', from file='%s', line number='%s', function='%s', code line='%s'"%(sys.exc_info()[1], exc[0], exc[1], exc[2], exc[3])
	return exc_mess

#-------------------------------------------------------------------------------

def do_the_stat(dog_id, depth):
	T = Tool(dog_id, depth)
	T.go()
	return T.get_result()

try:
	form = cgi.FieldStorage()
	if form.has_key("dog_id"):
		dog_id = form["dog_id"].value
		if form.has_key("depth"):
			depth = form["depth"].value
		else:
			depth = 5
		s = do_the_stat(dog_id, depth)
	else:
		s = "You entered an empty id"

	print "Content-Type: text/html\n"
	print """<html><HEAD><TITLE>swh stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in offsprings_stat: %s"%e









