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
	def __init__(self, dog_id, depth):
		self.DEEP_STOP = int(depth)+1
		
		if self.DEEP_STOP > 9:
			self.DEEP_STOP = 9

		self.DOG_ID = dog_id

		f = file("SWHDB", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.NO_ANCESTOR = ("data not available")
		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1280','border':2})

		if "+" in self.DOG_ID:
			self.mix = True
			self.DOG_ID1, self.DOG_ID2 = self.DOG_ID.split("+")
		else:
			self.mix = False

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

	def htmlprint_stat(self):
		try:
			if not self.mix:
				# dog name
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID) ; self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>COLOR</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>PRA</u></i>") ; self.table.setc(0, 8, "<i><u>DWARF GENE</u></i>") ; self.table.setc(0, 9, "<i><u>Country</u></i>") ; self.table.setc(0, 10, "<i><u>Birthday</u></i>"); self.table.setc(0, 11, "<i><u>Breeder</u></i>")
		    		self.table.setca(0,0,{'bgcolor':"#AA0000"})

				self.table.setc(1, 1, "<b><a href=%s>%s</a></b>"%("http://www.wolfdog.org/drupal/en/gallery/subcat/1/%s"%self.DOG_ID, self.dump_dict[self.DOG_ID]["NAME"]))

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

				self.table.setc(1, 8, self.dump_dict[self.DOG_ID]["DWARF"].replace("data not available", "?"))
				self.table.setc(1, 9, self.dump_dict[self.DOG_ID]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(1, 10, self.dump_dict[self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict[self.DOG_ID]["BIRTHDAY"]!="data not available":
					self.table.setc(1, 10, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[self.DOG_ID]["BIRTHDAY"],self.dump_dict[self.DOG_ID]["BIRTHDAY"]))
				else:
					self.table.setc(1, 10, self.dump_dict[self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(1, 11, self.dump_dict[self.DOG_ID]["BREEDER"].replace("data not available", "?"))
				self.table.setc(1, 11, self.dump_dict[self.DOG_ID]["BREEDER"].replace("data not available", "?"))

			else:
				# ---------------------------------- dog1 name
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID)

				self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>COLOR</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>PRA</u></i>") ; self.table.setc(0, 8, "<i><u>DWARF GENE</u></i>") ; self.table.setc(0, 9, "<i><u>Country</u></i>") ; self.table.setc(0, 10, "<i><u>Birthday</u></i>"); self.table.setc(0, 11, "<i><u>Breeder</u></i>")
		    		self.table.setca(0,0,{'bgcolor':"#AA0000"})


				self.table.setc(1, 1, "<b><a href=%s>%s</a></b>"%("http://www.wolfdog.org/drupal/en/gallery/subcat/1/%s"%self.DOG_ID1, self.dump_dict[self.DOG_ID1]["NAME"]))

				self.table.setc(1, 2, self.dump_dict[self.DOG_ID1]["GENDER"].replace("data not available", "?"))
				self.table.setc(1, 3, self.dump_dict[self.DOG_ID1]["COAT_COLOR"].replace("data not available", "?"))
				self.table.setc(1, 4, self.dump_dict[self.DOG_ID1]["INDEX_HEIGHT"].replace("data not available", "?"))
				self.table.setc(1, 5, self.dump_dict[self.DOG_ID1]["INDEX_FORMAT"].replace("data not available", "?"))

				self.table.setc(1, 6, self.dump_dict[self.DOG_ID1]["HIP"].replace("data not available", "?"))
				if self.dump_dict[self.DOG_ID1]["HIP"] != "data not available":
					if self.dump_dict[self.DOG_ID1]["HIP"][:1]=="E":
						self.table.setca(1, 6,{'bgcolor':"#992222"})
					if self.dump_dict[self.DOG_ID1]["HIP"][:1]=="D":
						self.table.setca(1, 6,{'bgcolor':"#994455"})
					if self.dump_dict[self.DOG_ID1]["HIP"][:1]=="C":
						self.table.setca(1, 6,{'bgcolor':"#886622"})
					if self.dump_dict[self.DOG_ID1]["HIP"][:1]=="B":
						self.table.setca(1, 6,{'bgcolor':"#559922"})
					if self.dump_dict[self.DOG_ID1]["HIP"][:1]=="A":
						self.table.setca(1, 6,{'bgcolor':"#229922"})

				self.table.setc(1, 7, self.dump_dict[self.DOG_ID1]["PRA"].replace("data not available", "?"))

				self.table.setc(1, 8, self.dump_dict[self.DOG_ID1]["DWARF"].replace("data not available", "?"))
				self.table.setc(1, 9, self.dump_dict[self.DOG_ID1]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(1, 10, self.dump_dict[self.DOG_ID1]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict[self.DOG_ID1]["BIRTHDAY"]!="data not available":
					self.table.setc(1, 10, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[self.DOG_ID1]["BIRTHDAY"],self.dump_dict[self.DOG_ID1]["BIRTHDAY"]))
				else:
					self.table.setc(1, 10, self.dump_dict[self.DOG_ID1]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(1, 11, self.dump_dict[self.DOG_ID1]["BREEDER"].replace("data not available", "?"))
				self.table.setc(1, 11, self.dump_dict[self.DOG_ID1]["BREEDER"].replace("data not available", "?"))

				# ------------------------------ dog2 name

				self.table.setc(2, 1, "<b><a href=%s>%s</a></b>"%("http://www.wolfdog.org/drupal/en/gallery/subcat/1/%s"%self.DOG_ID2, self.dump_dict[self.DOG_ID2]["NAME"]))

				self.table.setc(2, 2, self.dump_dict[self.DOG_ID2]["GENDER"].replace("data not available", "?"))
				self.table.setc(2, 3, self.dump_dict[self.DOG_ID2]["COAT_COLOR"].replace("data not available", "?"))
				self.table.setc(2, 4, self.dump_dict[self.DOG_ID2]["INDEX_HEIGHT"].replace("data not available", "?"))
				self.table.setc(2, 5, self.dump_dict[self.DOG_ID2]["INDEX_FORMAT"].replace("data not available", "?"))

				self.table.setc(2, 6, self.dump_dict[self.DOG_ID2]["HIP"].replace("data not available", "?"))
				if self.dump_dict[self.DOG_ID2]["HIP"] != "data not available":
					if self.dump_dict[self.DOG_ID2]["HIP"][:1]=="E":
						self.table.setca(2, 6,{'bgcolor':"#992222"})
					if self.dump_dict[self.DOG_ID2]["HIP"][:1]=="D":
						self.table.setca(2, 6,{'bgcolor':"#994455"})
					if self.dump_dict[self.DOG_ID2]["HIP"][:1]=="C":
						self.table.setca(2, 6,{'bgcolor':"#886622"})
					if self.dump_dict[self.DOG_ID2]["HIP"][:1]=="B":
						self.table.setca(2, 6,{'bgcolor':"#559922"})
					if self.dump_dict[self.DOG_ID2]["HIP"][:1]=="A":
						self.table.setca(2, 6,{'bgcolor':"#229922"})

				self.table.setc(2, 7, self.dump_dict[self.DOG_ID2]["PRA"].replace("data not available", "?"))

				self.table.setc(2, 8, self.dump_dict[self.DOG_ID2]["DWARF"].replace("data not available", "?"))
				self.table.setc(2, 9, self.dump_dict[self.DOG_ID2]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(2, 10, self.dump_dict[self.DOG_ID2]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict[self.DOG_ID2]["BIRTHDAY"]!="data not available":
					self.table.setc(2, 10, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[self.DOG_ID2]["BIRTHDAY"],self.dump_dict[self.DOG_ID2]["BIRTHDAY"]))
				else:
					self.table.setc(2, 10, self.dump_dict[self.DOG_ID2]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(2, 11, self.dump_dict[self.DOG_ID2]["BREEDER"].replace("data not available", "?"))
				self.table.setc(2, 11, self.dump_dict[self.DOG_ID2]["BREEDER"].replace("data not available", "?"))



			# stat
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"}) ; self.table.setc(3, 1, "for depth=%s"%str(int(self.DEEP_STOP)-1))




			# TODO check exist
			
			if not self.mix:
				DOG_ID_MOTHER = self.dump_dict[self.DOG_ID]["MOTHER"]
				DOG_ID_FATHER = self.dump_dict[self.DOG_ID]["FATHER"]
			else:
				#DOG_ID_MOTHER = self.dump_dict[self.DOG_ID1]["MOTHER"]
				#DOG_ID_FATHER = self.dump_dict[self.DOG_ID2]["FATHER"]
				DOG_ID_MOTHER = self.DOG_ID1
				DOG_ID_FATHER = self.DOG_ID2

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

							if (dog_key1 == dog_key2) and (dog_key1 not in ("d0.html", "d.html")):
								all_path.append(self.build_path(deep1, i, deep2, j, dog_key1 ))	
		
			# --- remove path
			final_path = []
			for apath in all_path:
			
				path_ok = True
				for p in all_path:
					#try:
					if apath[0][apath[1]-1] == p[0][p[1]] and apath[0][apath[1]+1] == p[0][p[1]]: # ca
						path_ok = False
						break
					#except: # fufu x fufu
					#		break

				if path_ok:
					final_path.append(apath)

			# --- coi
			res={}
			coi = 0
			for path in final_path:

				key = path[0][path[1]]

				ca_coi = (float(self.dump_dict[key]["COIFA"][:-1])/100.) + 1
				x = pow(0.5, len(path[0])) * ca_coi

				if res.has_key(key):
					res[key] += x
				else:
					res[key] = x

				coi += x

			coi*=100

			new_res = []
			for key in res:
				new_res.append( (res[key]*100, key) )
			
			new_res.sort(reverse=True)


	


			START = 4
			self.table.setc(START+1, 0, "<center><h3><b>COI</b></h3><i><h5>[Sum (1/2)^n1+n2+1 * (1+Fa)]<h5></i></center>")
			self.table.setc(START+1, 1, "<h3><b>%s%%</b></h3>"%coi)


			self.table.setc(START+2, 0, "<i><u>Name</u></i>") ; 
			self.table.setc(START+2, 1, "<i><u>Mother</u></i>")
			self.table.setc(START+2, 2, "<i><u>Father</u></i>")
			self.table.setc(START+2, 3, "<i><u>percent</u></i>")
			self.table.setc(START+2, 4, "<i><u>Gender</u></i>") 
			self.table.setc(START+2, 5, "<i><u>Birthday</u></i>")
			self.table.setc(START+2, 6, "<i><u>COLOR</u></i>")
			self.table.setc(START+2, 7, "<i><u>Idx H</u></i>")
			self.table.setc(START+2, 8, "<i><u>Idx F</u></i>")
			self.table.setc(START+2, 9, "<i><u>HD</u></i>")
			self.table.setc(START+2, 10, "<i><u>PRA</u></i>")
			self.table.setc(START+2, 11, "<i><u>DWARF GENE</u></i>")
			self.table.setc(START+2, 12, "<i><u>Country</u></i>")
			self.table.setc(START+2, 13, "<i><u>Breeder</u></i>")

			line=START+3
			i=0
			for elem in new_res:
				key=elem[1]
				percent=elem[0]

				self.table.setc(i+line, 0, "<a href=%s/saarloos.py?id=%s>%s</a>"%(SERVER, key, self.dump_dict[key]["NAME"]))

				abool=True
				if self.dump_dict[key]["NAME"] in ("FLEUR WOLVIN", "FLEUR II WOLVIN","WOLVIN"):
					self.table.setca(i+line, 0,{'bgcolor':"#223366"})
					abool=False
				elif re.search("F1", self.dump_dict[key]["NAME"]) or re.search("F2", self.dump_dict[key]["NAME"]) or re.search("F3", self.dump_dict[key]["NAME"]) or re.search("F4", self.dump_dict[key]["NAME"]) or re.search("F5", self.dump_dict[key]["NAME"]) or re.search("F6", self.dump_dict[key]["NAME"]):
					self.table.setca(i+line, 0,{'bgcolor':"#227766"})
					abool=False

				if abool:
					self.table.setca(i+line, 0,{'bgcolor':"#222233"})

				parent2_key = self.dump_dict[key]["MOTHER"]
				if parent2_key not in self.NO_ANCESTOR:
					self.table.setc(i+line, 1, "<h6><a href=%s/saarloos.py?id=%s>%s</a></h6>"%(SERVER, parent2_key,self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))

				parent2_key = self.dump_dict[key]["FATHER"]
				if parent2_key not in self.NO_ANCESTOR:
					self.table.setc(i+line, 2, "<h6><a href=%s/saarloos.py?id=%s>%s</a></h6>"%(SERVER, parent2_key,self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))

				self.table.setc(i+line, 3, "<b>%s%%</b>"%str(percent))
				self.table.setca(i+line, 3,{'bgcolor':"#222222"})

				self.table.setc(i+line,4, self.dump_dict[key]["GENDER"].replace("data not available", "?"))

				if self.dump_dict[key]["BIRTHDAY"]!="data not available":
					self.table.setc(i+line, 5, "<a href=%s/find_birth_saarloos.py?year=%s>%s</a>"%(SERVER, self.dump_dict[key]["BIRTHDAY"],self.dump_dict[key]["BIRTHDAY"]))
				else:
					self.table.setc(i+line, 5, self.dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))


				self.table.setc(i+line, 6, self.dump_dict[key]["COAT_COLOR"].replace("data not available", "?"))
				self.table.setc(i+line, 7, self.dump_dict[key]["INDEX_HEIGHT"].replace("data not available", "?"))
				self.table.setc(i+line, 8, self.dump_dict[key]["INDEX_FORMAT"].replace("data not available", "?"))

				# hip
				self.table.setc(i+line, 9, self.dump_dict[key]["HIP"].replace("data not available", "?"))
				if self.dump_dict[key]["HIP"][:1]=="E":
					self.table.setca(i+line, 9,{'bgcolor':"#992222"})
				if self.dump_dict[key]["HIP"][:1]=="D":
					self.table.setca(i+line, 9,{'bgcolor':"#994455"})
				if self.dump_dict[key]["HIP"][:1]=="C":
					self.table.setca(i+line, 9,{'bgcolor':"#886622"})
				if self.dump_dict[key]["HIP"][:1]=="B":
					self.table.setca(i+line, 9,{'bgcolor':"#559922"})
				if self.dump_dict[key]["HIP"][:1]=="A":
					self.table.setca(i+line, 9,{'bgcolor':"#229922"})

				self.table.setc(i+line, 10, self.dump_dict[key]["PRA"].replace("data not available", "?"))

				# coi
				self.table.setc(i+line, 11, self.dump_dict[key]["DWARF"].replace("data not available", "?"))

				self.table.setc(i+line, 12, self.dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))


				self.table.setc(i+line, 13, self.dump_dict[key]["BREEDER"].replace("data not available", "?"))

				i+=1


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













