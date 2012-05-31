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
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"}) ; self.table.setc(3, 1, " CZ breeding groups")

			# tree
			START = 4
			
			self.table.setc(START+1, 0, "<b>FATHER LINE</b>") ; self.table.setca(START+1,0,{'bgcolor':"#1111AA"})
			
			self.table.setc(START+1, 1, "<i><u>weight</u></i>")
			self.table.setc(START+1, 2, "<i><u>occurrence</u></i>")
			self.table.setc(START+1, 3, "<i><u>shortest distance</u></i>")

			self.table.setc(START+2, 0, "Gar z Ros�kova (I)".decode("iso-8859-2").encode("utf-8")); 
			self.table.setc(START+3, 0, "C�zar od Pavli&#353;ina (II)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+4, 0, "K�j z Ros�kova (II)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+5, 0, "Binc Pohostinstvo (III)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+6, 0, "Candiff Pohostinstvo (III)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+7, 0, "Astor Motovsk� dvor (IV)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+8, 0, "Bak z Dou&#353;ova dvora (V)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+9, 0, "Barry z Dou&#353;ova dvora (V)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+10, 0, "Amur z D�blova kanonu (VI)".decode("iso-8859-2").encode("utf-8"));
			
			self.table.setc(START+11, 0, "Ariska Recn� CS (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+12, 0, "Cira z Dou&#353;ova dvora (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+13, 0, "Cita z Dou&#353;ova dvora (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+14, 0, "Arm�n Recn� CS (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			
			self.table.setc(START+15, 0, "Alan Brevnovsk� stopa (VIII)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START+16, 0, "Ajax Brevnovsk� stopa (VIII)".decode("iso-8859-2").encode("utf-8"));
				
			
			START2 = 21
			
				
			self.table.setc(START2+1, 0, "<b>MOTHER LINE</b>") ; self.table.setca(START2+1,0,{'bgcolor':"#BB5533"})
			
			self.table.setc(START2+1, 1, "<i><u>weight</u></i>")
			self.table.setc(START2+1, 2, "<i><u>occurrence</u></i>")
			self.table.setc(START2+1, 3, "<i><u>shortest distance</u></i>")

			self.table.setc(START2+2, 0, "Gar z Ros�kova (I)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+3, 0, "C�zar od Pavli&#353;ina (II)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+4, 0, "K�j z Ros�kova (II)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+5, 0, "Binc Pohostinstvo (III)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+6, 0, "Candiff Pohostinstvo (III)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+7, 0, "Astor Motovsk� dvor (IV)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+8, 0, "Bak z Dou&#353;ova dvora (V)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+9, 0, "Barry z Dou&#353;ova dvora (V)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+10, 0, "Amur z D�blova kanonu (VI)".decode("iso-8859-2").encode("utf-8"));
			
			self.table.setc(START2+11, 0, "Ariska Recn� CS (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+12, 0, "Cira z Dou&#353;ova dvora (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+13, 0, "Cita z Dou&#353;ova dvora (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+14, 0, "Arm�n Recn� CS (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			
			self.table.setc(START2+15, 0, "Alan Brevnovsk� stopa (VIII)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START2+16, 0, "Ajax Brevnovsk� stopa (VIII)".decode("iso-8859-2").encode("utf-8"));
			

			START3 = 38
			
				
			self.table.setc(START3+1, 0, "<b>FATHER + MOTHER LINE</b>") ; self.table.setca(START3+1,0,{'bgcolor':"#55BB33"})
			
			self.table.setc(START3+1, 1, "<i><u>weight</u></i>")
			self.table.setc(START3+1, 2, "<i><u>occurrence</u></i>")
			self.table.setc(START3+1, 3, "<i><u>shortest distance</u></i>")

			self.table.setc(START3+2, 0, "Gar z Ros�kova (I)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+3, 0, "C�zar od Pavli&#353;ina (II)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+4, 0, "K�j z Ros�kova (II)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+5, 0, "Binc Pohostinstvo (III)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+6, 0, "Candiff Pohostinstvo (III)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+7, 0, "Astor Motovsk� dvor (IV)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+8, 0, "Bak z Dou&#353;ova dvora (V)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+9, 0, "Barry z Dou&#353;ova dvora (V)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+10, 0, "Amur z D�blova kanonu (VI)".decode("iso-8859-2").encode("utf-8"));
			
			self.table.setc(START3+11, 0, "Ariska Recn� CS (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+12, 0, "Cira z Dou&#353;ova dvora (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+13, 0, "Cita z Dou&#353;ova dvora (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+14, 0, "Arm�n Recn� CS (VII Kazan PS)".decode("iso-8859-2").encode("utf-8"));
			
			self.table.setc(START3+15, 0, "Alan Brevnovsk� stopa (VIII)".decode("iso-8859-2").encode("utf-8"));
			self.table.setc(START3+16, 0, "Ajax Brevnovsk� stopa (VIII)".decode("iso-8859-2").encode("utf-8"));
			
			# ----- father line
			# dog: proportion, shortest, nb occ
			resf = { "gar":[0,99,0], "cezar":[0,99,0], "kaj":[0,99,0], "binc":[0,99,0], "candiff":[0,99,0], "astor":[0,99,0], "barry":[0,99,0], "bak":[0,99,0], "amur":[0,99,0], "alan":[0,99,0], "ajax":[0,99,0], "ariska":[0,99,0], "cira":[0,99,0], "cita":[0,99,0], "armin":[0,99,0] }
			
			for deep in self.ancestor_dict_father:
				dogs_list = self.ancestor_dict_father[deep]
				
				#Gar z Ros�kova CS = 891	
				if "d891.html" in dogs_list:
					self.check_dog(resf, "gar", deep)
					
				#C�zar od Pavli�ina = 938	
				if "d938.html" in dogs_list:
					self.check_dog(resf, "cezar", deep)
				
				#K�j z Ros�kova = 929	
				if "d929.html" in dogs_list:
					self.check_dog(resf, "kaj", deep)
					
				#Binc Pohostinstvo = 922	
				if "d922.html" in dogs_list:
					self.check_dog(resf, "binc", deep)
	
				#Candiff Pohostinstvo = 930	
				if "d930.html" in dogs_list:
					self.check_dog(resf, "candiff", deep)
			
				#Astor Motovsk� dvor = 876
				if "d876.html" in dogs_list:
					self.check_dog(resf, "astor", deep)
					
				#Barry z Dou�ova dvora CS = 886
				if "d886.html" in dogs_list:
					self.check_dog(resf, "barry", deep)
					
				#bak z Dou�ova dvora CS = 885
				if "d885.html" in dogs_list:
					self.check_dog(resf, "bak", deep)					

				#Amur z D�blova kanonu = 796
				if "d796.html" in dogs_list:
					self.check_dog(resf, "amur", deep)	
					
				#Alan Brevnovsk� stopa = 746
				if "d746.html" in dogs_list:
					self.check_dog(resf, "alan", deep)					
				
				#Ajax Brevnovsk� stopa = 744
				if "d744.html" in dogs_list:
					self.check_dog(resf, "ajax", deep)

				#Ariska Recn� CS 914
				if "d914.html" in dogs_list:
					self.check_dog(resf, "ariska", deep)
					
				#Cira z Dou�ova dvora CS 846
				if "d846.html" in dogs_list:
					self.check_dog(resf, "cira", deep)
					
				#Cita z Dou�ova dvora CS 924
				if "d924.html" in dogs_list:
					self.check_dog(resf, "cita", deep)
					
				#Arm�n Recn� CS 912
				if "d912.html" in dogs_list:
					self.check_dog(resf, "armin", deep)
					

			self.display(resf, "gar", START+2, 1);
			
			self.display(resf, "cezar", START+3, 1);
			self.display(resf, "kaj", START+4, 1);
			
			self.display(resf, "binc", START+5, 1);
			self.display(resf, "candiff", START+6, 1);
			
			self.display(resf, "astor", START+7, 1);
			
			self.display(resf, "barry", START+8, 1);
			self.display(resf, "bak", START+9, 1);
			
			self.display(resf, "amur", START+10, 1);
			
			self.display(resf, "ariska", START+11, 1);
			self.display(resf, "cira", START+12, 1);
			self.display(resf, "cita", START+13, 1);
			self.display(resf, "armin", START+14, 1);
		
			self.display(resf, "alan", START+15, 1);
			self.display(resf, "ajax", START+16, 1);

			
		
			# ----- mother line
			# dog: proportion, shortest, nb occ
			resm = { "gar":[0,99,0], "cezar":[0,99,0], "kaj":[0,99,0], "binc":[0,99,0], "candiff":[0,99,0], "astor":[0,99,0], "barry":[0,99,0], "bak":[0,99,0], "amur":[0,99,0], "alan":[0,99,0], "ajax":[0,99,0], "ariska":[0,99,0], "cira":[0,99,0], "cita":[0,99,0], "armin":[0,99,0] }
			
			for deep in self.ancestor_dict_mother:
				dogs_list = self.ancestor_dict_mother[deep]
				
				#Gar z Ros�kova CS = 891	
				if "d891.html" in dogs_list:
					self.check_dog(resm, "gar", deep)
					
				#C�zar od Pavli�ina = 938	
				if "d938.html" in dogs_list:
					self.check_dog(resm, "cezar", deep)
				
				#K�j z Ros�kova = 929	
				if "d929.html" in dogs_list:
					self.check_dog(resm, "kaj", deep)
					
				#Binc Pohostinstvo = 922	
				if "d922.html" in dogs_list:
					self.check_dog(resm, "binc", deep)
	
				#Candiff Pohostinstvo = 930	
				if "d930.html" in dogs_list:
					self.check_dog(resm, "candiff", deep)
			
				#Astor Motovsk� dvor = 876
				if "d876.html" in dogs_list:
					self.check_dog(resm, "astor", deep)
					
				#Barry z Dou�ova dvora CS = 886
				if "d886.html" in dogs_list:
					self.check_dog(resm, "barry", deep)
					
				#bak z Dou�ova dvora CS = 885
				if "d885.html" in dogs_list:
					self.check_dog(resm, "bak", deep)					

				#Amur z D�blova kanonu = 796
				if "d796.html" in dogs_list:
					self.check_dog(resm, "amur", deep)	
					
				#Alan Brevnovsk� stopa = 746
				if "d746.html" in dogs_list:
					self.check_dog(resm, "alan", deep)					
				
				#Ajax Brevnovsk� stopa = 744
				if "d744.html" in dogs_list:
					self.check_dog(resm, "ajax", deep)

				#Ariska Recn� CS 914
				if "d914.html" in dogs_list:
					self.check_dog(resm, "ariska", deep)
					
				#Cira z Dou�ova dvora CS 846
				if "d846.html" in dogs_list:
					self.check_dog(resm, "cira", deep)
					
				#Cita z Dou�ova dvora CS 924
				if "d924.html" in dogs_list:
					self.check_dog(resm, "cita", deep)
					
				#Arm�n Recn� CS 912
				if "d912.html" in dogs_list:
					self.check_dog(resm, "armin", deep)
					

			self.display(resm, "gar", START2+2, 1);
			
			self.display(resm, "cezar", START2+3, 1);
			self.display(resm, "kaj", START2+4, 1);
			
			self.display(resm, "binc", START2+5, 1);
			self.display(resm, "candiff", START2+6, 1);
			
			self.display(resm, "astor", START2+7, 1);
			
			self.display(resm, "barry", START2+8, 1);
			self.display(resm, "bak", START2+9, 1);
			
			self.display(resm, "amur", START2+10, 1);
			
			self.display(resm, "ariska", START2+11, 1);
			self.display(resm, "cira", START2+12, 1);
			self.display(resm, "cita", START2+13, 1);
			self.display(resm, "armin", START2+14, 1);
		
			self.display(resm, "alan", START2+15, 1);
			self.display(resm, "ajax", START2+16, 1);

						
			# mother + father line
			
			resfm = {}
			
			for key in resm:
				resfm[key] = resm[key]
				
				resfm[key][0] += resf[key][0]
				
				if resfm[key][1] > resf[key][1]:
					resfm[key][1] = resf[key][1]
					
				resfm[key][2] += resf[key][2]
		
			self.display(resfm, "gar", START3+2, 1);
			
			self.display(resfm, "cezar", START3+3, 1);
			self.display(resfm, "kaj", START3+4, 1);
			
			self.display(resfm, "binc", START3+5, 1);
			self.display(resfm, "candiff", START3+6, 1);
			
			self.display(resfm, "astor", START3+7, 1);
			
			self.display(resfm, "barry", START3+8, 1);
			self.display(resfm, "bak", START3+9, 1);
			
			self.display(resfm, "amur", START3+10, 1);
			
			self.display(resfm, "ariska", START3+11, 1);
			self.display(resfm, "cira", START3+12, 1);
			self.display(resfm, "cita", START3+13, 1);
			self.display(resfm, "armin", START3+14, 1);
		
			self.display(resfm, "alan", START3+15, 1);
			self.display(resfm, "ajax", START3+16, 1);
			
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
			depth = 99
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













