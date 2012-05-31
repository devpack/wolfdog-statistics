#! /usr/bin/python
# -*- coding: utf-8 -*-

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
	def __init__(self, dog_id, depth, dog_list, sorted):
		self.DEEP_STOP = int(depth)
		self.DOG_ID = dog_id.replace(" ", "")
		
		if dog_list:
			self.DOG_LIST = dog_list.replace(" ", "")
			self.DOG_LIST = self.DOG_LIST.split(",")
		else:
			self.DOG_LIST = None
			
		self.SORT = sorted
			
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

			# only father
			fkey = self.dump_dict["d%s.html"%self.DOG_ID]["FATHER"]
			self.ancestor_dict_father = {0: "d%s.html"%self.DOG_ID, 1:fkey}
			self.tree_parse_father(fkey, 1)

			# only mother
			mkey = self.dump_dict["d%s.html"%self.DOG_ID]["MOTHER"]
			self.ancestor_dict_mother = {0: "d%s.html"%self.DOG_ID, 1:mkey}
			self.tree_parse_mother(mkey, 1)
			
		# + mix +
		else:
		
			# only father
			if self.dump_dict["d%s.html"%self.DOG_ID1]["GENDER"]=="Male":
				fkey = "d%s.html"%self.DOG_ID1
			else:
				fkey = "d%s.html"%self.DOG_ID2
				
			self.ancestor_dict_father = {0: self.DOG_ID, 1:fkey}
			self.tree_parse_father(fkey, 1)		

			# only mother
			if self.dump_dict["d%s.html"%self.DOG_ID1]["GENDER"]=="Female":
				mkey = "d%s.html"%self.DOG_ID1
			else:
				mkey = "d%s.html"%self.DOG_ID2
				
			self.ancestor_dict_mother = {0: self.DOG_ID, 1:mkey}
			self.tree_parse_mother(mkey, 1)	
						
			#print self.ancestor_dict, "<br>"
			#print "<br>"


		self.htmlprint_stat()

	#-----------------------------------------------------------------------

	def htmlprint_stat(self):
		try:
			if not self.mix:
				# dog name
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID) ; self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Bonitation</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>ED</u></i>") ; self.table.setc(0, 8, "<i><u>COI5G</u></i>") ; self.table.setc(0, 9, "<i><u>AVK5G</u></i>"); self.table.setc(0, 10, "<i><u>Country</u></i>") ; self.table.setc(0, 11, "<i><u>Birthday</u></i>"); self.table.setc(0, 12, "<i><u>Breeder</u></i>")
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

				self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Bonitation</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>ED</u></i>") ; self.table.setc(0, 8, "<i><u>COI5G</u></i>") ; self.table.setc(0, 9, "<i><u>AVK5G</u></i>"); self.table.setc(0, 10, "<i><u>Country</u></i>") ; self.table.setc(0, 11, "<i><u>Birthday</u></i>"); self.table.setc(0, 12, "<i><u>Breeder</u></i>")
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
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"}) ; self.table.setc(3, 1, "New breeding groups")

			# tree
			START = 4
			
			group_list = (891,938,929,922,930,876,886,885,796,746,744,914,846,924,912)
			group_list = (622, 940, 796, 928, 938, 852, 765, 948, 937, 945, 935, 1044, 1095, 939, 929, 947, 787, 772, 3584, 1307, 781, 1184, 769, 788, 239, 166, 766, 957, 839, 577, 408, 81, 770, 5431, 1041, 745, 1037, 768, 966, 727, 744, 954, 747, 950, 646, 254, 953, 3551, 164, 746)
			if self.DOG_LIST:
				group_list=self.DOG_LIST
				
			# FATHER -------------------------------------------------------------------------------------------------------------------------------
			indice0 = START+1
			self.table.setc(indice0, 0, "<b>FATHER LINE</b>") ; self.table.setca(indice0,0,{'bgcolor':"#1111AA"})
			self.table.setc(indice0, 1, "<i><u>weight</u></i>")
			self.table.setc(indice0, 2, "<i><u>occurrence</u></i>")
			self.table.setc(indice0, 3, "<i><u>shortest distance</u></i>")

			# dog: proportion, shortest, nb occ
			resf = {}
			for dog in group_list:
				resf["d%s.html"%dog] = [0,99,0]
			
			for deep in self.ancestor_dict_father:
				dogs_list = self.ancestor_dict_father[deep]
				
				for dog in group_list:
					if "d%s.html"%dog in dogs_list:
						self.check_dog(resf, "d%s.html"%dog, deep)
						
			if self.SORT:
				group_list_sorted=[]
				for dog in group_list:
					group_list_sorted.append((resf["d%s.html"%dog][0], dog))
				
				group_list_sorted.sort(reverse=True)
				
				for i, dog in enumerate(group_list_sorted):
					self.display(resf, "d%s.html"%dog[1], indice0 +1 +i, 1);
					self.table.setc(indice0 +1 +i, 0, self.dump_dict["d%s.html"%dog[1]]["NAME"]); 
					
			else:
			
				for i, dog in enumerate(group_list):
					self.display(resf, "d%s.html"%dog, indice0 +1 +i, 1);
					self.table.setc(indice0 +1 +i, 0, self.dump_dict["d%s.html"%dog]["NAME"]); 
				
			# MOTHER -------------------------------------------------------------------------------------------------------------------------------
			indice1 = START+3+i
			self.table.setc(indice1, 0, "<b>MOTHER LINE</b>") ; self.table.setca(indice1,0,{'bgcolor':"#BB5533"})
			self.table.setc(indice1, 1, "<i><u>weight</u></i>")
			self.table.setc(indice1, 2, "<i><u>occurrence</u></i>")
			self.table.setc(indice1, 3, "<i><u>shortest distance</u></i>")		

			# dog: proportion, shortest, nb occ
			resm = {}
			for dog in group_list:
				resm["d%s.html"%dog] = [0,99,0]
			
			for deep in self.ancestor_dict_mother:
				dogs_list = self.ancestor_dict_mother[deep]
				
				for dog in group_list:
					if "d%s.html"%dog in dogs_list:
						self.check_dog(resm, "d%s.html"%dog, deep)

			if self.SORT:
				group_list_sorted=[]
				for dog in group_list:
					group_list_sorted.append((resm["d%s.html"%dog][0], dog))
				
				group_list_sorted.sort(reverse=True)
				
				for j, dog in enumerate(group_list_sorted):
					self.display(resm, "d%s.html"%dog[1], indice1+1+j, 1);
					self.table.setc(indice1+1+j, 0, self.dump_dict["d%s.html"%dog[1]]["NAME"]); 
					
			else:
				for j, dog in enumerate(group_list):
					self.display(resm, "d%s.html"%dog, indice1+1+j, 1);
					self.table.setc(indice1+1+j, 0, self.dump_dict["d%s.html"%dog]["NAME"]); 	
				
			# FATHER + MOTHER -----------------------------------------------------------------------------------------------------------------------				
			indice2 = START+5+i+j
			self.table.setc(indice2, 0, "<b>FATHER + MOTHER LINE</b>") ; self.table.setca(indice2,0,{'bgcolor':"#55BB33"})
			self.table.setc(indice2, 1, "<i><u>weight</u></i>")
			self.table.setc(indice2, 2, "<i><u>occurrence</u></i>")
			self.table.setc(indice2, 3, "<i><u>shortest distance</u></i>")			
				
			resfm = {}
			for key in resm:
				resfm[key] = resm[key]
				
				resfm[key][0] += resf[key][0]
				
				if resfm[key][1] > resf[key][1]:
					resfm[key][1] = resf[key][1]
					
				resfm[key][2] += resf[key][2]
				
			if self.SORT:
				group_list_sorted=[]
				for dog in group_list:
					group_list_sorted.append((resfm["d%s.html"%dog][0], dog))
				
				group_list_sorted.sort(reverse=True)
				
				for k, dog in enumerate(group_list_sorted):
					self.display(resfm, "d%s.html"%dog[1], indice2+1+k, 1);
					self.table.setc(indice2+1+k, 0, self.dump_dict["d%s.html"%dog[1]]["NAME"]); 
					
			else:
				for k, dog in enumerate(group_list):
					self.display(resfm, "d%s.html"%dog, indice2+1+k, 1);
					self.table.setc(indice2+1+k, 0, self.dump_dict["d%s.html"%dog]["NAME"]); 	
				
		except Exception, e:
			print "Content-Type: text/html\n"
			print "Error htmlprint_stat: %s"%e
			print exc_detail()

					
	#-----------------------------------------------------------------------
			
	def check_dog(self, dico, name, deep):
	
		dico[name][0] += 1./pow(2, deep)
		
		if dico[name][1] > deep:
			dico[name][1] = deep
			
		dico[name][2] += 1
			
	#-----------------------------------------------------------------------
			
	def display(self, dico, name, posx, posy):
	
		if dico[name][0] != 0:
			self.table.setc(posx, posy, "%s"%str(float(dico[name][0])*100)) ;
		else:
			self.table.setc(posx, posy, "%s"%"X") ;

		if dico[name][2] != 0:
			self.table.setc(posx, posy+1, "%s"%dico[name][2]) ;
		else:
			self.table.setc(posx, posy+1, "%s"%"X") ;

		if dico[name][1] != 99:
			self.table.setc(posx, posy+2, "%s"%dico[name][1]) ;
		else:
			self.table.setc(posx, posy+2, "%s"%"X") ;
				
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
			
	#-----------------------------------------------------------------------

	def tree_parse_father(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			# mother
			mkey = self.dump_dict[node_key]["MOTHER"]
			if mkey not in self.NO_ANCESTOR:
				if self.ancestor_dict_father.has_key(deep+1):
					self.ancestor_dict_father[deep+1].append(mkey)
				else:
					self.ancestor_dict_father[deep+1] = [mkey]

				self.tree_parse_father(mkey, deep+1)

			# father
			fkey = self.dump_dict[node_key]["FATHER"]
			if fkey not in self.NO_ANCESTOR:
				if self.ancestor_dict_father.has_key(deep+1):
					self.ancestor_dict_father[deep+1].append(fkey)
				else:
					self.ancestor_dict_father[deep+1] = [fkey]

				self.tree_parse_father(fkey, deep+1)

		except Exception, e:
			print "Content-Type: text/html\n"
			print exc_detail()
	
	def tree_parse_mother(self, node_key, deep):
		if deep==self.DEEP_STOP:
			return

		try:
			# mother
			mkey = self.dump_dict[node_key]["MOTHER"]
			if mkey not in self.NO_ANCESTOR:
				if self.ancestor_dict_mother.has_key(deep+1):
					self.ancestor_dict_mother[deep+1].append(mkey)
				else:
					self.ancestor_dict_mother[deep+1] = [mkey]

				self.tree_parse_mother(mkey, deep+1)

			# father
			fkey = self.dump_dict[node_key]["FATHER"]
			if fkey not in self.NO_ANCESTOR:
				if self.ancestor_dict_mother.has_key(deep+1):
					self.ancestor_dict_mother[deep+1].append(fkey)
				else:
					self.ancestor_dict_mother[deep+1] = [fkey]

				self.tree_parse_mother(fkey, deep+1)

		except Exception, e:
			print "Content-Type: text/html\n"
			print exc_detail()
			
#-------------------------------------------------------------------------------

def exc_detail():
	exc = tb.extract_tb(sys.exc_info()[2])[0]
	exc_mess = "Exception type='%s', from file='%s', line number='%s', function='%s', code line='%s'"%(sys.exc_info()[1], exc[0], exc[1], exc[2], exc[3])
	return exc_mess


def do_the_stat(dog_id, depth, dog_list, sorted):
	T = Tool(dog_id, depth, dog_list, sorted)
	T.go()
	return T.get_result()

try:
	form = cgi.FieldStorage()
	if form.has_key("dog_id"):
		dog_id = form["dog_id"].value
		if form.has_key("depth"):
			depth = form["depth"].value
		else:
			depth = 99
		if form.has_key("dog_list"):
			dog_list = form["dog_list"].value
		else:
			dog_list = None
		if form.has_key("sorted"):
			sorted = True
		else:
			sorted = False
		s = do_the_stat(dog_id, depth, dog_list, sorted)
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













