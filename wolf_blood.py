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

		self.wolf_proportion = {}
		self.wolf_distance = {}
		self.gsd_proportion = {}
		self.gsd_distance = {}

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
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID) ; self.table.setc(0, 1, "<i><u>Name</u></i>") ; self.table.setc(0, 2, "<i><u>Gender</u></i>") ; self.table.setc(0, 3, "<i><u>Bonitation</u></i>") ; self.table.setc(0, 4, "<i><u>Idx H</u></i>") ; self.table.setc(0, 5, "<i><u>Idx F</u></i>") ; self.table.setc(0, 6, "<i><u>HD</u></i>") ; self.table.setc(0, 7, "<i><u>ED</u></i>") ; self.table.setc(0, 8, "<i><u>COI5G</u></i>") ; self.table.setc(0, 9, "<i><u>Country</u></i>") ; self.table.setc(0, 10, "<i><u>Birthday</u></i>"); self.table.setc(0, 11, "<i><u>Breeder</u></i>")
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
				self.table.setc(1, 9, self.dump_dict["d%s.html"%self.DOG_ID]["ORIGIN COUNTRY"].replace("data not available", "?"))

				#self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"]!="data not available":
					self.table.setc(1, 10, "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"],self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"]))
				else:
					self.table.setc(1, 10, self.dump_dict["d%s.html"%self.DOG_ID]["BIRTHDAY"].replace("data not available", "?"))

				#self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"].replace("data not available", "?"))
				if self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"]!="data not available":
					self.table.setc(1, 11, "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"].replace(" ", "%20"), self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"]))
				else:
					self.table.setc(1, 11, self.dump_dict["d%s.html"%self.DOG_ID]["BREEDER"].replace("data not available", "?"))

			# ---------- mix
			else:
				# ---------------------------------- dog1 name
				self.table.setc(0, 0, "<b>ID=%s</b>"%self.DOG_ID)

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
			self.table.setc(3, 0, "<b>STATISTIC</b>") ; self.table.setca(3,0,{'bgcolor':"#AAAA11"})

			# tree		

			START = 4
			self.table.setc(START+1, 0, "<h3><b>Wolf blood</b></h3>")

			if not self.mix:
				self.table.setc(START+1, 1, "<h3><b>%s%%</b></h3>"%self.wp("d%s.html"%self.DOG_ID, 0))

			else:
				self.table.setc(START+1, 1, "<h3><b>%s%%</b></h3>"%self.wp2(self.ancestor_dict[1][0], self.ancestor_dict[1][1],0))

			# wolf distance			
			self.table.setc(START+3, 0, "<i><b>%s</b></i>"%"Wolf")
			self.table.setc(START+3, 1, "<i><b>%s</b></i>"%"Contribution")
			self.table.setc(START+3, 2, "<i><b>%s</b></i>"%"Shortest distance")

			# wolf proportion
			wsum=0
			for wkey in self.wolf_proportion:
				wsum += self.wolf_proportion[wkey]

			wl=[]
			for wkey in self.wolf_proportion:
				wl.append((self.wolf_proportion[wkey], wkey))

			wl.sort(reverse=True)

			o=0
			for elem in wl:
				self.table.setc(START+4+o, 0, "%s"%elem[1])
				self.table.setca(START+4+o, 0,{'bgcolor':"#223366"})

				self.table.setc(START+4+o, 1, "%s%%"%str(elem[0]*100./wsum))
				self.table.setc(START+4+o, 2, "%s"%str(self.wolf_distance[elem[1]]-1))
				o+=1

			# gsd distance			
			self.table.setc(START+4+o+1, 0, "<i><b>%s</b></i>"%"GSD")
			self.table.setc(START+4+o+1, 1, "<i><b>%s</b></i>"%"Contribution")
			self.table.setc(START+4+o+1, 2, "<i><b>%s</b></i>"%"Shortest distance")

			# gsd proportion
			gsum=0
			for gkey in self.gsd_proportion:
				gsum += self.gsd_proportion[gkey]

			gl=[]
			for gkey in self.gsd_proportion:
				gl.append((self.gsd_proportion[gkey], gkey))

			gl.sort(reverse=True)

			oo=0
			for elem in gl:
				self.table.setc(START+4+o+2+oo, 0, "%s"%elem[1])
				self.table.setca(START+4+o+2+oo, 0,{'bgcolor':"#227766"})

				self.table.setc(START+4+o+2+oo, 1, "%s%%"%str(elem[0]*100./gsum))
				self.table.setc(START+4+o+2+oo, 2, "%s"%str(self.gsd_distance[elem[1]]-1))
				oo+=1

		except Exception, e:
			print "Content-Type: text/html\n"
			print "Error htmlprint_stat: %s"%e
			print exc_detail()

	#-----------------------------------------------------------------------

	def isgsd(self, dog_id, deep=1):
		name = self.dump_dict[dog_id]["NAME"]
		if name.find("---NO---") >= 0:
			if self.gsd_proportion.has_key(name):
				self.gsd_proportion[name] += 1./pow(2, deep)
				if self.gsd_distance[name] > deep:
					self.gsd_distance[name] = deep
			else:
				self.gsd_proportion[name] = 1./pow(2, deep)
				self.gsd_distance[name] = deep
			return True

	def is_halfwolf(self, dog_id, deep=1):
		if dog_id == "d1534.html":
			if self.wolf_proportion.has_key("X wolf"):
				self.wolf_proportion["X wolf"] += 1./pow(2, deep+1)
				if self.wolf_distance["X wolf"] > deep+1:
					self.wolf_distance["X wolf"] = deep+1
			else:
				self.wolf_proportion["X wolf"] = 1./pow(2, deep+1)
				self.wolf_distance["X wolf"] = deep+1
			return True

	def iswolf(self, dog_id, deep=1):
		if self.dump_dict[dog_id]["NAME"] == "Lejdy ___Canis Lupus Lupus___":
			if self.wolf_proportion.has_key("Lejdy"):
				self.wolf_proportion["Lejdy"] += 1./pow(2, deep)
				if self.wolf_distance["Lejdy"] > deep:
					self.wolf_distance["Lejdy"] = deep
			else:
				self.wolf_proportion["Lejdy"] = 1./pow(2, deep)
				self.wolf_distance["Lejdy"] = deep
			return True

		if self.dump_dict[dog_id]["NAME"] == "Brita ___Canis Lupus Lupus___":
			if self.wolf_proportion.has_key("Brita"):
				self.wolf_proportion["Brita"] += 1./pow(2, deep)
				if self.wolf_distance["Brita"] > deep:
					self.wolf_distance["Brita"] = deep
			else:
				self.wolf_proportion["Brita"] = 1./pow(2, deep)
				self.wolf_distance["Brita"] = deep
			return True

		if self.dump_dict[dog_id]["NAME"] == "Argo ___Canis Lupus Lupus___":
			if self.wolf_proportion.has_key("Argo"):
				self.wolf_proportion["Argo"] += 1./pow(2, deep)
				if self.wolf_distance["Argo"] > deep:
					self.wolf_distance["Argo"] = deep
			else:
				self.wolf_proportion["Argo"] = 1./pow(2, deep)
				self.wolf_distance["Argo"] = deep
			return True

		if self.dump_dict[dog_id]["NAME"].encode("hex")=="c5a06172696b205f5f5f43616e6973204c75707573204c757075735f5f5f":
			if self.wolf_proportion.has_key("Sarik"):
				self.wolf_proportion["Sarik"] += 1./pow(2, deep)
				if self.wolf_distance["Sarik"] > deep:
					self.wolf_distance["Sarik"] = deep
			else:
				self.wolf_proportion["Sarik"] = 1./pow(2, deep)
				self.wolf_distance["Sarik"] = deep
			return True

		if self.dump_dict[dog_id]["NAME"].encode("hex")=="4c7570c3ad6e61205f5f5f43616e6973206c75707573206f63636964656e74616c69735f5f5f":
			if self.wolf_proportion.has_key("Lupina"):
				self.wolf_proportion["Lupina"] += 1./pow(2, deep)
				if self.wolf_distance["Lupina"] > deep:
					self.wolf_distance["Lupina"] = deep
			else:
				self.wolf_proportion["Lupina"] = 1./pow(2, deep)
				self.wolf_distance["Lupina"] = deep
			return True



		else:
			return False

	#-----------------------------------------------------------------------

	def wp2(self, mkey, fkey, deep):
		deep+=1

		if (mkey not in self.NO_ANCESTOR) and (fkey not in self.NO_ANCESTOR):
			return ( self.wp(mkey, deep)+self.wp(fkey, deep) ) / 2.

		if (mkey in self.NO_ANCESTOR) and (fkey in self.NO_ANCESTOR):
			if self.iswolf(dog_id, deep):
				return 100
			if self.isgsd(dog_id, deep):
				return 0
			if self.is_halfwolf(dog_id, deep):
				return 50
			return 0

		if (mkey not in self.NO_ANCESTOR) and (fkey in self.NO_ANCESTOR):
			return ( self.wp(mkey, deep) ) / 2.

		if (fkey not in self.NO_ANCESTOR):
			return ( self.wp(fkey, deep) ) / 2.

	#-----------------------------------------------------------------------

	def wp(self, dog_id, deep):
		deep+=1

		mkey = self.dump_dict[dog_id]["MOTHER"]
		fkey = self.dump_dict[dog_id]["FATHER"]

		#if dog_id == "d1534.html":
		#	mkey = "d0.html"
		#	fkey = "d0.html"

		if (mkey not in self.NO_ANCESTOR) and (fkey not in self.NO_ANCESTOR):
			return ( self.wp(mkey, deep)+self.wp(fkey, deep) ) / 2.

		if (mkey in self.NO_ANCESTOR) and (fkey in self.NO_ANCESTOR):
			if self.iswolf(dog_id, deep):
				return 100
			if self.isgsd(dog_id, deep):
				return 0
			if self.is_halfwolf(dog_id, deep):
				return 50
			return 0

		if (mkey in self.NO_ANCESTOR):
			if self.iswolf(dog_id, deep):
				return 100
			if self.isgsd(dog_id, deep):
				return 0
			if self.is_halfwolf(dog_id, deep):
				return 50
			return 0

		if (fkey in self.NO_ANCESTOR):
			if self.iswolf(dog_id, deep):
				return 100
			if self.isgsd(dog_id, deep):
				return 0
			if self.is_halfwolf(dog_id, deep):
				return 50
			return 0

		if (mkey not in self.NO_ANCESTOR) and (fkey in self.NO_ANCESTOR):
			return ( self.wp(mkey, deep) ) / 2.

		if (fkey not in self.NO_ANCESTOR):
			return ( self.wp(fkey, deep) ) / 2.

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
		s = do_the_stat(dog_id, 99)
	else:
		s = "You entered an empty id"

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/space2.jpg'>"""
	print """%s"""%s
	print """</body></html>"""

except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in wolfblood_stat: %s"%e













