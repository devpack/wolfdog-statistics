#! /usr/bin/python

import cgi, os, sys, urllib, time, pprint, re, datetime

try:
	import cPickle as pck
except ImportError:
	import pickle as pck

import traceback as tb
import PyHtmlTable

SERVER = "http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Tool(object):
	def __init__(self, dog_id1, dog_id2, depth):
		self.DEEP_STOP = int(depth)+1
		
		if self.DEEP_STOP > 8:
			self.DEEP_STOP = 8

		self.DOG_ID1 = dog_id1
		self.DOG_ID2 = dog_id2

		f = file("WDDB_utf8", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.NO_ANCESTOR = ("d0.html", "d.html")
		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})

	#-----------------------------------------------------------------------

	def go(self):
		self.htmlprint_stat()

	#-----------------------------------------------------------------------

	def build_path(self, deep1, pos1, deep2, pos2, cakey):
		apath = []

		while 1:
			off = self.the_off(self.ancestor_dict1, deep1, pos1)
			if off != -1:
				apath.append(off)
				deep1 -= 1
				pos1 = pos1/2
			else:
				apath.reverse()
				break

		ca_pos = len(apath)
		apath.append(cakey)

		while 1:
			off = self.the_off(self.ancestor_dict2, deep2, pos2)
			if off != -1:
				apath.append(off)
				deep2 -= 1
				pos2 = pos2/2
			else:
				break

		return apath, ca_pos

	#-----------------------------------------------------------------------

	def the_off(self, adict, deep, pos):
		if deep-1 != 0:
			return adict[deep-1][pos/2]
		else:
			return -1
	#-----------------------------------------------------------------------

	def calc_coi(self, DOG_ID1, DOG_ID2=0):

		if DOG_ID2 == 0:
			DOG_ID_MOTHER = self.dump_dict["d%s.html"%DOG_ID1]["MOTHER"]
			DOG_ID_FATHER = self.dump_dict["d%s.html"%DOG_ID1]["FATHER"]	
		else:
			DOG_ID_MOTHER = "d%s.html"%DOG_ID1
			DOG_ID_FATHER = "d%s.html"%DOG_ID2

		self.ancestor_dict1 = {1: [DOG_ID_MOTHER]}
		self.tree_parse1(DOG_ID_MOTHER, 1)

		self.ancestor_dict2 = {1: [DOG_ID_FATHER]}
		self.tree_parse2(DOG_ID_FATHER, 1)
	
		# --- find common_ancestors
		all_path = []
		for deep1 in self.ancestor_dict1:
			for i, dog_key1 in enumerate(self.ancestor_dict1[deep1]):

				for deep2 in self.ancestor_dict2:
					for j, dog_key2 in enumerate(self.ancestor_dict2[deep2]):

						if (dog_key1 == dog_key2) and (dog_key1 not in self.NO_ANCESTOR):
							all_path.append(self.build_path(deep1, i, deep2, j, dog_key1 ))	
	
		# --- remove path
		final_path = []
		for apath in all_path:
		
			path_ok = True
			for p in all_path:
				try:
					if apath[0][apath[1]-1] == p[0][p[1]] and apath[0][apath[1]+1] == p[0][p[1]]: # ca
						path_ok = False
						break
				except: # fufu x fufu
						break

			if path_ok:
				final_path.append(apath)

		# --- coi
		coi = 0
		for path in final_path:
			key = path[0][path[1]]

			ca_coi = (float(self.dump_dict[key]["COIFA"][:-1])/100.) + 1
			coi += pow(0.5, len(path[0])) * ca_coi


		return coi

	#-----------------------------------------------------------------------

	def htmlprint_stat(self):
		try:
			# ---------------------------------- dog1 name
			self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID1)

			self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Bonitation</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>ED</u></i>") ; self.table.setc(0, 8, "<i><u>COI5G</u></i>") ; self.table.setc(0, 9, "<i><u>Country</u></i>") ; self.table.setc(0, 10, "<i><u>Birthday</u></i>"); self.table.setc(0, 11, "<i><u>Breeder</u></i>")
	    		self.table.setca(0,0,{'bgcolor':"#AA0000"})


			self.table.setc(1, 1, "<b><a href=%s>%s</a></b>"%("http://www.wolfdog.org/drupal/en/gallery/subcat/1/%s"%self.DOG_ID1, self.dump_dict["d%s.html"%self.DOG_ID1]["NAME"]))

			self.table.setc(1, 2, self.dump_dict["d%s.html"%self.DOG_ID1]["GENDER"].replace("data not available", "?"))
			self.table.setc(1, 3, self.dump_dict["d%s.html"%self.DOG_ID1]["BONITATION"].replace("data not available", "?"))
			self.table.setc(1, 4, self.dump_dict["d%s.html"%self.DOG_ID1]["INDEX_HEIGHT"].replace("data not available", "?"))
			self.table.setc(1, 5, self.dump_dict["d%s.html"%self.DOG_ID1]["INDEX_FORMAT"].replace("data not available", "?"))

			self.table.setc(1, 6, self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"] != "data not available":
				if self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"][:1]=="E":
					self.table.setca(1, 6,{'bgcolor':"#992222"})
				if self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"][:1]=="D":
					self.table.setca(1, 6,{'bgcolor':"#994455"})
				if self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"][:1]=="C":
					self.table.setca(1, 6,{'bgcolor':"#886622"})
				if self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"][:1]=="B":
					self.table.setca(1, 6,{'bgcolor':"#559922"})
				if self.dump_dict["d%s.html"%self.DOG_ID1]["HIP"][:1]=="A":
					self.table.setca(1, 6,{'bgcolor':"#229922"})

			self.table.setc(1, 7, self.dump_dict["d%s.html"%self.DOG_ID1]["ED"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID1]["ED"] != "data not available":
				if self.dump_dict["d%s.html"%self.DOG_ID1]["ED"] == "0-0":
					self.table.setca(1, 7,{'bgcolor':"#229922"})
				ed_val = self.dump_dict["d%s.html"%self.DOG_ID1]["ED"].split("-")
				if "3" in ed_val:
					self.table.setca(1, 7,{'bgcolor':"#992222"})			
				if "2" in ed_val:
					self.table.setca(1, 7,{'bgcolor':"#994455"})
				if "1" in ed_val:
					self.table.setca(1, 7,{'bgcolor':"#886622"})

			self.table.setc(1, 8, self.dump_dict["d%s.html"%self.DOG_ID1]["COI5G"].replace("data not available", "?"))
			self.table.setc(1, 9, self.dump_dict["d%s.html"%self.DOG_ID1]["ORIGIN COUNTRY"].replace("data not available", "?"))

			#self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"]!="data not available":
				self.table.setc(1, 10, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"],self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"]))
			else:
				self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"].replace("data not available", "?"))

			#self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"]!="data not available":
				self.table.setc(1, 11, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"].replace(" ", "%20"), self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"]))
			else:
				self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"].replace("data not available", "?"))

			# ------------------------------ dog2 name

			self.table.setc(2, 1, "<b><a href=%s>%s</a></b>"%("http://www.wolfdog.org/drupal/en/gallery/subcat/1/%s"%self.DOG_ID2, self.dump_dict["d%s.html"%self.DOG_ID2]["NAME"]))

			self.table.setc(2, 2, self.dump_dict["d%s.html"%self.DOG_ID2]["GENDER"].replace("data not available", "?"))
			self.table.setc(2, 3, self.dump_dict["d%s.html"%self.DOG_ID2]["BONITATION"].replace("data not available", "?"))
			self.table.setc(2, 4, self.dump_dict["d%s.html"%self.DOG_ID2]["INDEX_HEIGHT"].replace("data not available", "?"))
			self.table.setc(2, 5, self.dump_dict["d%s.html"%self.DOG_ID2]["INDEX_FORMAT"].replace("data not available", "?"))

			self.table.setc(2, 6, self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"] != "data not available":
				if self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"][:1]=="E":
					self.table.setca(2, 6,{'bgcolor':"#992222"})
				if self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"][:1]=="D":
					self.table.setca(2, 6,{'bgcolor':"#994455"})
				if self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"][:1]=="C":
					self.table.setca(2, 6,{'bgcolor':"#886622"})
				if self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"][:1]=="B":
					self.table.setca(2, 6,{'bgcolor':"#559922"})
				if self.dump_dict["d%s.html"%self.DOG_ID2]["HIP"][:1]=="A":
					self.table.setca(2, 6,{'bgcolor':"#229922"})

			self.table.setc(2, 7, self.dump_dict["d%s.html"%self.DOG_ID2]["ED"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID2]["ED"] != "data not available":
				if self.dump_dict["d%s.html"%self.DOG_ID2]["ED"] == "0-0":
					self.table.setca(2, 7,{'bgcolor':"#229922"})
				ed_val = self.dump_dict["d%s.html"%self.DOG_ID2]["ED"].split("-")
				if "3" in ed_val:
					self.table.setca(2, 7,{'bgcolor':"#992222"})			
				if "2" in ed_val:
					self.table.setca(2, 7,{'bgcolor':"#994455"})
				if "1" in ed_val:
					self.table.setca(2, 7,{'bgcolor':"#886622"})

			self.table.setc(2, 8, self.dump_dict["d%s.html"%self.DOG_ID2]["COI5G"].replace("data not available", "?"))
			self.table.setc(2, 9, self.dump_dict["d%s.html"%self.DOG_ID2]["ORIGIN COUNTRY"].replace("data not available", "?"))

			#self.table.setc(2, 10, self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"]!="data not available":
				self.table.setc(2, 10, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"],self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"]))
			else:
				self.table.setc(2, 10, self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"].replace("data not available", "?"))

			#self.table.setc(2, 11, self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"].replace("data not available", "?"))
			if self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"]!="data not available":
				self.table.setc(2, 11, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"].replace(" ", "%20"), self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"]))
			else:
				self.table.setc(2, 11, self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"].replace("data not available", "?"))



			# stat
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"}) ; self.table.setc(3, 1, "for depth=%s"%str(int(self.DEEP_STOP)-1))


			icab = self.calc_coi(self.DOG_ID1, self.DOG_ID2)
			ica  = self.calc_coi(self.DOG_ID1)
			icb  = self.calc_coi(self.DOG_ID2)

			rc = float(2*icab) / pow((1+ica)*(1+icb), 0.5)
			rc *= 100

			START = 4
			self.table.setc(START+1, 0, "<h3><b>RC</b></h3>")
			self.table.setc(START+1, 1, "<h3><b>%s%%</b></h3>"%rc)

		except Exception, e:
			print "Content-Type: text/html\n"
			print "Error htmlprint_stat: %s"%e
			print exc_detail()

	#-----------------------------------------------------------------------

	def get_result(self):
		res = ""
		res += """<html><body BGCOLOR="#00000" TEXT="#FFFFFF" LINK="#FFFFFF" VLINK="#FFFFFF" ALINK="#FFFFFF">"""
		res += """<head><style type="text/css"><!--a {text-decoration: none;}--></style></head>"""
		res += self.table.return_html()
		res += """</body></html>"""
		return res

#-------------------------------------------------------------------------------

	def tree_parse(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			# mother
			try:
				mkey = self.dump_dict[node_key]["MOTHER"]
			except:
				mkey = "d0.html"

			if self.ancestor_dict.has_key(deep+1):
				self.ancestor_dict[deep+1].append(mkey)
			else:
				self.ancestor_dict[deep+1] = [mkey]

			self.tree_parse(mkey, deep+1)

			# father
			try:
				fkey = self.dump_dict[node_key]["FATHER"]
			except:
				fkey = "d0.html"

			if self.ancestor_dict.has_key(deep+1):
				self.ancestor_dict[deep+1].append(fkey)
			else:
				self.ancestor_dict[deep+1] = [fkey]

			self.tree_parse(fkey, deep+1)

		except Exception, e:
			print "Content-Type: text/html\n"
			print exc_detail()


	def tree_parse1(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			# mother
			try:
				mkey = self.dump_dict[node_key]["MOTHER"]
			except:
				mkey = "d0.html"

			if self.ancestor_dict1.has_key(deep+1):
				self.ancestor_dict1[deep+1].append(mkey)
			else:
				self.ancestor_dict1[deep+1] = [mkey]

			self.tree_parse1(mkey, deep+1)

			# father
			try:
				fkey = self.dump_dict[node_key]["FATHER"]
			except:
				fkey = "d0.html"

			if self.ancestor_dict1.has_key(deep+1):
				self.ancestor_dict1[deep+1].append(fkey)
			else:
				self.ancestor_dict1[deep+1] = [fkey]

			self.tree_parse1(fkey, deep+1)

		except Exception, e:
			print "Content-Type: text/html\n"
			print exc_detail()


	def tree_parse2(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			# mother
			try:
				mkey = self.dump_dict[node_key]["MOTHER"]
			except:
				mkey = "d0.html"


			if self.ancestor_dict2.has_key(deep+1):
				self.ancestor_dict2[deep+1].append(mkey)
			else:
				self.ancestor_dict2[deep+1] = [mkey]

			self.tree_parse2(mkey, deep+1)

			# father
			try:
				fkey = self.dump_dict[node_key]["FATHER"]
			except:
				fkey = "d0.html"

			if self.ancestor_dict2.has_key(deep+1):
				self.ancestor_dict2[deep+1].append(fkey)
			else:
				self.ancestor_dict2[deep+1] = [fkey]

			self.tree_parse2(fkey, deep+1)

		except Exception, e:
			print "Content-Type: text/html\n"
			print exc_detail()

#-------------------------------------------------------------------------------

def exc_detail():
	exc = tb.extract_tb(sys.exc_info()[2])[0]
	exc_mess = "Exception type='%s', from file='%s', line number='%s', function='%s', code line='%s'"%(sys.exc_info()[1], exc[0], exc[1], exc[2], exc[3])
	return exc_mess


def do_the_stat(dog_id1, dog_id2, depth):
	T = Tool(dog_id1, dog_id2, depth)
	T.go()
	return T.get_result()

try:
	form = cgi.FieldStorage()
	if form.has_key("dog_id1") and form.has_key("dog_id2"):
		dog_id1 = form["dog_id1"].value
		dog_id2 = form["dog_id2"].value
		if form.has_key("depth"):
			depth = form["depth"].value
		else:
			depth = 5
		s = do_the_stat(dog_id1, dog_id2, depth)
	else:
		s = "<h3>%s</h3>"%"You entered an empty ID for a dog."

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body TEXT="#FFFFFF" background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'></body>"""
	print """%s"""%s
	print """</html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in offsprings_stat: %s"%e













