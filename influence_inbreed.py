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
		self.DEEP_STOP = int(depth)
		self.DOG_ID = dog_id.replace(" ", "")

		f = file("WDDB_utf8", 'rb')
		self.dump_dict = pck.load(f)
		f.close()

		self.NO_ANCESTOR = ("d0.html", "d.html")
		self.table  = PyHtmlTable.PyHtmlTable(1, 1, {'width':'1400','border':2})

		if "+" in self.DOG_ID:
			self.mix = True
			self.DOG_ID1, self.DOG_ID2 = self.DOG_ID.split("+")
		else:
			self.mix = False

	#-----------------------------------------------------------------------

	def go(self):
		if not self.mix:
			self.ancestor_dict = {0: "d%s.html"%self.DOG_ID}
			self.tree_parse("d%s.html"%self.DOG_ID, 0)
		else:
			self.ancestor_dict1 = {1: ["d%s.html"%self.DOG_ID1]}
			self.tree_parse1("d%s.html"%self.DOG_ID1, 1)

			self.ancestor_dict2 = {1: ["d%s.html"%self.DOG_ID2]}
			self.tree_parse2("d%s.html"%self.DOG_ID2, 1)

			self.ancestor_dict = {0: self.DOG_ID}
			if len(self.ancestor_dict1) > len(self.ancestor_dict2):
				for key in self.ancestor_dict1:
					try:
						self.ancestor_dict[key] = self.ancestor_dict1[key] + self.ancestor_dict2[key]
					except:
						self.ancestor_dict[key] = self.ancestor_dict1[key]

			else:
				for key in self.ancestor_dict2:
					try:
						self.ancestor_dict[key] = self.ancestor_dict2[key] + self.ancestor_dict1[key]
					except:
						self.ancestor_dict[key] = self.ancestor_dict2[key]


			#print self.ancestor_dict, "<br>"
			#print "<br>"


		self.htmlprint_stat()

	#-----------------------------------------------------------------------

	def htmlprint_stat(self):
		try:
			if not self.mix:
				# dog name
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID) ; self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Bonitation</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>ED</u></i>") ; self.table.setc(0, 8, "<i><u>COI5G</u></i>"); self.table.setc(0, 9, "<i><u>AVK5G</u></i>") ; self.table.setc(0, 10, "<i><u>Country</u></i>") ; self.table.setc(0, 11, "<i><u>Birthday</u></i>"); self.table.setc(0, 12, "<i><u>Breeder</u></i>")
		    		self.table.setca(0,0,{'bgcolor':"#AA0000"})


				self.table.setc(1, 1, "<b><a href=%s>%s</a></b>"%("http://www.wolfdog.org/drupal/en/gallery/subcat/1/%s"%self.DOG_ID, self.dump_dict["d%s.html"%self.DOG_ID]["NAME"]))

				self.table.setc(1, 2, self.dump_dict["d%s.html"%self.DOG_ID]["GENDER"].replace("data not available", "?"))
				self.table.setc(1, 3, self.dump_dict["d%s.html"%self.DOG_ID]["BONITATION"].replace("data not available", "?"))
				self.table.setc(1, 4, self.dump_dict["d%s.html"%self.DOG_ID]["INDEX_HEIGHT"].replace("data not available", "?"))
				self.table.setc(1, 5, self.dump_dict["d%s.html"%self.DOG_ID]["INDEX_FORMAT"].replace("data not available", "?"))

				self.table.setc(1, 6, self.dump_dict["d%s.html"%self.DOG_ID]["HIP"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID]["HIP"] != "data not available":
					if self.dump_dict["d%s.html"%self.DOG_ID]["HIP"][:1]=="E":
						self.table.setca(1, 6,{'bgcolor':"#992222"})
					if self.dump_dict["d%s.html"%self.DOG_ID]["HIP"][:1]=="D":
						self.table.setca(1, 6,{'bgcolor':"#994455"})
					if self.dump_dict["d%s.html"%self.DOG_ID]["HIP"][:1]=="C":
						self.table.setca(1, 6,{'bgcolor':"#886622"})
					if self.dump_dict["d%s.html"%self.DOG_ID]["HIP"][:1]=="B":
						self.table.setca(1, 6,{'bgcolor':"#559922"})
					if self.dump_dict["d%s.html"%self.DOG_ID]["HIP"][:1]=="A":
						self.table.setca(1, 6,{'bgcolor':"#229922"})

				self.table.setc(1, 7, self.dump_dict["d%s.html"%self.DOG_ID]["ED"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID]["ED"] != "data not available":
					if self.dump_dict["d%s.html"%self.DOG_ID]["ED"] == "0-0":
						self.table.setca(1, 7,{'bgcolor':"#229922"})
					ed_val = self.dump_dict["d%s.html"%self.DOG_ID]["ED"].split("-")
					if "3" in ed_val:
						self.table.setca(1, 7,{'bgcolor':"#992222"})			
					if "2" in ed_val:
						self.table.setca(1, 7,{'bgcolor':"#994455"})
					if "1" in ed_val:
						self.table.setca(1, 7,{'bgcolor':"#886622"})

				self.table.setc(1, 8, self.dump_dict["d%s.html"%self.DOG_ID]["COI5G"].replace("data not available", "?"))
				self.table.setc(1, 9, self.dump_dict["d%s.html"%self.DOG_ID]["AVK5G"].replace("data not available", "?"))
				self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"]!="data not available":
					self.table.setc(1, 11, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"],self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"]))
				else:
					self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"]!="data not available":
					self.table.setc(1, 12, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"].replace(" ", "%20"), self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"]))
				else:
					self.table.setc(1, 12, self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"].replace("data not available", "?"))

			# ---------- mix
			else:
				# ---------------------------------- dog1 name
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID)

				self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Bonitation</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>ED</u></i>") ; self.table.setc(0, 8, "<i><u>COI5G</u></i>"); self.table.setc(0, 9, "<i><u>AVK5G</u></i>") ; self.table.setc(0, 10, "<i><u>Country</u></i>") ; self.table.setc(0, 11, "<i><u>Birthday</u></i>"); self.table.setc(0, 12, "<i><u>Breeder</u></i>")
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
				self.table.setc(1, 9, self.dump_dict["d%s.html"%self.DOG_ID1]["AVK5G"].replace("data not available", "?"))

				self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID1]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"]!="data not available":
					self.table.setc(1, 11, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"],self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"]))
				else:
					self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID1]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"]!="data not available":
					self.table.setc(1, 12, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"].replace(" ", "%20"), self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"]))
				else:
					self.table.setc(1, 12, self.dump_dict["d%s.html"%self.DOG_ID1]["BREEDER"].replace("data not available", "?"))

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
				self.table.setc(2, 9, self.dump_dict["d%s.html"%self.DOG_ID2]["AVK5G"].replace("data not available", "?"))

				self.table.setc(2, 10, self.dump_dict["d%s.html"%self.DOG_ID2]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(2, 10, self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"]!="data not available":
					self.table.setc(2, 11, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"],self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"]))
				else:
					self.table.setc(2, 11, self.dump_dict["d%s.html"%self.DOG_ID2]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(2, 11, self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"]!="data not available":
					self.table.setc(2, 12, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"].replace(" ", "%20"), self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"]))
				else:
					self.table.setc(2, 12, self.dump_dict["d%s.html"%self.DOG_ID2]["BREEDER"].replace("data not available", "?"))


			# stat
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"}) ; self.table.setc(3, 1, "for depth=%s"%self.DEEP_STOP)

			# tree
			START = 4
			self.table.setc(START+1, 0, "<i><u>Name</u></i>") ; 
			self.table.setc(START+1, 1, "<i><u>Mother</u></i>")
			self.table.setc(START+1, 2, "<i><u>Father</u></i>")
			self.table.setc(START+1, 3, "<i><u>influence inbreed</u></i>")
			self.table.setc(START+1, 4, "<i><u>weight</u></i>")
			self.table.setc(START+1, 5, "<i><u>number</u></i>")
			self.table.setc(START+1, 6, "<i><u>Gender</u></i>") 
			self.table.setc(START+1, 7, "<i><u>Birthday</u></i>")
			self.table.setc(START+1, 8, "<i><u>Bonitation</u></i>")
			self.table.setc(START+1, 9, "<i><u>Idx H</u></i>")
			self.table.setc(START+1, 10, "<i><u>Idx F</u></i>")
			self.table.setc(START+1, 11, "<i><u>HD</u></i>")
			self.table.setc(START+1, 12, "<i><u>ED</u></i>")
			self.table.setc(START+1, 13, "<i><u>COI5G</u></i>")
			self.table.setc(START+1, 14, "<i><u>AVK5G</u></i>")
			self.table.setc(START+1, 15, "<i><u>Country</u></i>")
			self.table.setc(START+1, 16, "<i><u>Breeder</u></i>")


			res_weight = {}
			res_nb = {}

			for deep in self.ancestor_dict:
				if deep != 0:
					for ancetre_key in self.ancestor_dict[deep]:
				
						if res_weight.has_key(ancetre_key):
							res_weight[ancetre_key] += float(1) / pow(2,deep)
							res_nb[ancetre_key] += 1
						else:
							res_weight[ancetre_key] = float(1) / pow(2,deep)
							res_nb[ancetre_key] = 1

			#print res_weight
			#print res_nb

			new_res = []
			for key in res_weight:
				try:
					if res_nb[key]!=1:
						new_res.append((res_weight[key], res_nb[key], key))
				except Exception, e:
					print "Content-Type: text/html\n"
					print e

			new_res.sort(reverse=True)

			sum=0
			for elem in new_res:
				sum += float(elem[0])

			line=START+3
			i=0
			for elem in new_res:
				key=elem[2]
				percent=(float(elem[0])*100)/sum
				weight=elem[0]
				nb=elem[1]
				self.table.setc(i+line, 0, "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, key.split(".")[0][1:], self.dump_dict[key]["NAME"]))

				abool=True
				if self.dump_dict[key]["NAME"] in ("Lejdy ___Canis Lupus Lupus___", "Brita ___Canis Lupus Lupus___", "Argo ___Canis Lupus Lupus___") or self.dump_dict[key]["NAME"].encode("hex")=="c5a06172696b205f5f5f43616e6973204c75707573204c757075735f5f5f":
					self.table.setca(i+line, 0,{'bgcolor':"#223366"})
					abool=False
				elif re.search("F1", self.dump_dict[key]["NAME"]) or re.search("F2", self.dump_dict[key]["NAME"]) or re.search("F3", self.dump_dict[key]["NAME"]) or re.search("F4", self.dump_dict[key]["NAME"]) or re.search("F5", self.dump_dict[key]["NAME"]) or re.search("F6", self.dump_dict[key]["NAME"]):
					self.table.setca(i+line, 0,{'bgcolor':"#227766"})
					abool=False

				if abool:
					self.table.setca(i+line, 0,{'bgcolor':"#222233"})

				parent2_key = self.dump_dict[key]["MOTHER"].replace("data not available", "?")
				if parent2_key not in self.NO_ANCESTOR:
					self.table.setc(i+line, 1, "<h6><a href=%s/form.py?id=%s>%s</a></h6>"%(SERVER, parent2_key.split(".")[0][1:],self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))

				parent2_key = self.dump_dict[key]["FATHER"].replace("data not available", "?")
				if parent2_key not in self.NO_ANCESTOR:
					self.table.setc(i+line, 2, "<h6><a href=%s/form.py?id=%s>%s</a></h6>"%(SERVER, parent2_key.split(".")[0][1:],self.dump_dict[parent2_key]["NAME"].replace("data not available", "?")))

				self.table.setc(i+line, 3, "<b>%s%%</b>"%str(percent))
				self.table.setca(i+line, 3,{'bgcolor':"#222222"})

				self.table.setc(i+line, 4, "%s"%str(weight))
				self.table.setc(i+line, 5, "%s"%str(nb))

				self.table.setc(i+line, 6, self.dump_dict[key]["GENDER"].replace("data not available", "?"))

				if self.dump_dict[key]["BIRTHDAY"]!="data not available":
					self.table.setc(i+line, 7, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict[key]["BIRTHDAY"],self.dump_dict[key]["BIRTHDAY"]))
				else:
					self.table.setc(i+line, 7, self.dump_dict[key]["BIRTHDAY"].replace("data not available", "?"))


				self.table.setc(i+line, 8, self.dump_dict[key]["BONITATION"].replace("data not available", "?"))
				self.table.setc(i+line, 9, self.dump_dict[key]["INDEX_HEIGHT"].replace("data not available", "?"))
				self.table.setc(i+line, 10, self.dump_dict[key]["INDEX_FORMAT"].replace("data not available", "?"))

				# hip
				self.table.setc(i+line, 11, self.dump_dict[key]["HIP"].replace("data not available", "?"))
				if self.dump_dict[key]["HIP"][:1]=="E":
					self.table.setca(i+line, 11,{'bgcolor':"#992222"})
				if self.dump_dict[key]["HIP"][:1]=="D":
					self.table.setca(i+line, 11,{'bgcolor':"#994455"})
				if self.dump_dict[key]["HIP"][:1]=="C":
					self.table.setca(i+line, 11,{'bgcolor':"#886622"})
				if self.dump_dict[key]["HIP"][:1]=="B":
					self.table.setca(i+line, 11,{'bgcolor':"#559922"})
				if self.dump_dict[key]["HIP"][:1]=="A":
					self.table.setca(i+line, 11,{'bgcolor':"#229922"})

				self.table.setc(i+line, 12, self.dump_dict[key]["ED"].replace("data not available", "?"))
				if self.dump_dict[key]["ED"] != "data not available":
					if self.dump_dict[key]["ED"] == "0-0":
						self.table.setca(i+line, 12,{'bgcolor':"#229922"})
					ed_val = self.dump_dict[key]["ED"].split("-")
					if "3" in ed_val:
						self.table.setca(i+line, 12,{'bgcolor':"#992222"})			
					if "2" in ed_val:
						self.table.setca(i+line, 12,{'bgcolor':"#994455"})
					if "1" in ed_val:
						self.table.setca(i+line, 12,{'bgcolor':"#886622"})

				# coi
				self.table.setc(i+line, 13, self.dump_dict[key]["COI5G"].replace("data not available", "?"))
				if self.dump_dict[key]["COI5G"] == "0%":
					self.table.setca(i+line, 13,{'bgcolor':"#7733155"})

				self.table.setc(i+line, 14, self.dump_dict[key]["AVK5G"].replace("data not available", "?"))
				if self.dump_dict[key]["AVK5G"] == "100.0%":
					self.table.setca(i+line, 14,{'bgcolor':"#7733155"})

				self.table.setc(i+line, 15, self.dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?"))


				if self.dump_dict[key]["BREEDER"]!="data not available":
					self.table.setc(i+line, 16, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict[key]["BREEDER"].replace(" ", "%20"), self.dump_dict[key]["BREEDER"]))
				else:
					self.table.setc(i+line, 16, self.dump_dict[key]["BREEDER"].replace("data not available", "?"))


				#print "(key: %s)"%elem[2], "%s%%"%((float(elem[0])*100)/sum), " ", "(weight: %s)"%elem[0], "(nb: %s)"%elem[1]
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

	#-----------------------------------------------------------------------

	def tree_parse(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			# mother
			mkey = self.dump_dict[node_key]["MOTHER"]
			if mkey not in self.NO_ANCESTOR:
				if self.ancestor_dict.has_key(deep+1):
					self.ancestor_dict[deep+1].append(mkey)
				else:
					self.ancestor_dict[deep+1] = [mkey]

				self.tree_parse(mkey, deep+1)

			# father
			fkey = self.dump_dict[node_key]["FATHER"]
			if fkey not in self.NO_ANCESTOR:
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
			mkey = self.dump_dict[node_key]["MOTHER"]
			if mkey not in self.NO_ANCESTOR:
				if self.ancestor_dict1.has_key(deep+1):
					self.ancestor_dict1[deep+1].append(mkey)
				else:
					self.ancestor_dict1[deep+1] = [mkey]

				self.tree_parse1(mkey, deep+1)

			# father
			fkey = self.dump_dict[node_key]["FATHER"]
			if fkey not in self.NO_ANCESTOR:
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
			mkey = self.dump_dict[node_key]["MOTHER"]
			if mkey not in self.NO_ANCESTOR:
				if self.ancestor_dict2.has_key(deep+1):
					self.ancestor_dict2[deep+1].append(mkey)
				else:
					self.ancestor_dict2[deep+1] = [mkey]

				self.tree_parse2(mkey, deep+1)

			# father
			fkey = self.dump_dict[node_key]["FATHER"]
			if fkey not in self.NO_ANCESTOR:
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
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in offsprings_stat: %s"%e













