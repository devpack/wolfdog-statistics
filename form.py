#! /usr/bin/python
import cgi, time

try:
	import cPickle as pck
except ImportError:
	import pickle as pck

SERVER = "http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin"

def add_dog_info(k, val):
	x = ""
	
	x+= """<tr><td align="right">%s&nbsp;&nbsp;</td>"""%k
	x+= """<td align="left"><i>%s</i></td>""" % val
	x+= """</tr>""" 
	
	return x


def form_print(id=0):

	if id !=0:
		f = file("WDDB_utf8", 'rb')
		dump_dict = pck.load(f)
		f.close()

		dog_name = dump_dict["d%s.html"%id]["NAME"].replace("'", " ")

		link_str = """<a href=http://www.wolfdog.org/site/fr/gallery/cat/1/0/%s>More pictures of this dog</a><br>"""%id

		s = "" 		

		try:
			key = "d%s.html"%str(id)
			s += """<table><tr><td><img src="http://dl.wolfdog.org/pics/dbase/%s.jpg" border=0><br><i><h5><p align="center">%s</p></h5></i></td>"""%(id,link_str)

		except:
			s += """<table><tr><td><img src="http://dl.wolfdog.org/pics/dbase/n.jpg"<br><i><h5><p align="center">%s</p></h5></i></td>"""%(link_str)

		s+= """<td>"""

		s+= """<table>"""

		s += add_dog_info( "Name: ", dump_dict[key]["NAME"].replace("data not available", "?") ) 

		if dump_dict[key]["BIRTHDAY"]!="data not available":
			s += add_dog_info( "Birthday: ", "<a href=%s/find_birth.py?year=%s>%s</a>"%(SERVER, dump_dict[key]["BIRTHDAY"],dump_dict[key]["BIRTHDAY"]) ) 
		else:
			s += add_dog_info( "Birthday: ", dump_dict[key]["BIRTHDAY"].replace("data not available", "?") ) 
		
		s += add_dog_info( "Gender: ", dump_dict[key]["GENDER"].replace("data not available", "?") ) 

		if dump_dict[key]["MOTHER"] not in ("d0.html", "d.html", "?", "data not available"):
			s += add_dog_info( "Mother: ", "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, dump_dict[key]["MOTHER"].split(".")[0][1:],dump_dict[dump_dict[key]["MOTHER"]]["NAME"].replace("data not available", "?")) ) 
		else:
			s += add_dog_info( "Mother: ", dump_dict[key]["MOTHER"].replace("d0.html", "?").replace("d.html", "?") ) 

		if dump_dict[key]["FATHER"] not in ("d0.html", "d.html", "?", "data not available"):
			s += add_dog_info( "Father: ", "<a href=%s/form.py?id=%s>%s</a>"%(SERVER, dump_dict[key]["FATHER"].split(".")[0][1:],dump_dict[dump_dict[key]["FATHER"]]["NAME"].replace("data not available", "?")) ) 
		else:
			s += add_dog_info( "Father: ", dump_dict[key]["FATHER"].replace("d0.html", "?").replace("d.html", "?") ) 

		s += add_dog_info( "COI5G: ", dump_dict[key]["COI5G"].replace("data not available", "?") ) 
		s += add_dog_info( "COI8G: ", dump_dict[key]["COIFA"].replace("data not available", "?") ) 
		s += add_dog_info( "AVK5G: ", dump_dict[key]["AVK5G"].replace("data not available", "?") ) 
		s += add_dog_info( "AVK8G: ", dump_dict[key]["AVK8G"].replace("data not available", "?") ) 
		s += add_dog_info( "HD: ", dump_dict[key]["HIP"].replace("data not available", "?") ) 
		s += add_dog_info( "ED: ", dump_dict[key]["ED"].replace("data not available", "?") ) 
		s += add_dog_info( "PRA: ", dump_dict[key]["PRA"].replace("data not available", "?") ) 
		s += add_dog_info( "Bonitation: ", dump_dict[key]["BONITATION"].replace("data not available", "?") ) 
		#s += add_dog_info( "Coat Color: ", dump_dict[key]["COAT_COLOR"].replace("data not available", "?") ) 
		#s += add_dog_info( "Coat Lenght: ", dump_dict[key]["COAT_LENGHT"].replace("data not available", "?") ) 
		s += add_dog_info( "Breeder: ", "<a href=%s/find_breeders.py?name=%s>%s</a>"%(SERVER, dump_dict[key]["BREEDER"].replace(" ", "%20"), dump_dict[key]["BREEDER"].replace("data not available", "?")) ) 

		if dump_dict[key]["LIVING COUNTRY"]!="France" and dump_dict[key]["LIVING COUNTRY"]!="data not available":
			s += add_dog_info( "Owner: ", dump_dict[key]["OWNER"].replace("data not available", "?") ) 

		s += add_dog_info( "Training: ", dump_dict[key]["TRAINING"].replace("data not available", "?") ) 

		if dump_dict[key]["ORIGIN COUNTRY"]!="data not available":
			s += add_dog_info( "Origin Country: ", "<a href=%s/living_country.py?country=%s>%s</a>"%(SERVER, dump_dict[key]["ORIGIN COUNTRY"],dump_dict[key]["ORIGIN COUNTRY"]) ) 
		else:
			s += add_dog_info( "Origin Country: ", dump_dict[key]["ORIGIN COUNTRY"].replace("data not available", "?") ) 

		if dump_dict[key]["LIVING COUNTRY"]!="data not available":
			s += add_dog_info( "Living Country: ", "<a href=%s/living_country.py?country=%s>%s</a>"%(SERVER, dump_dict[key]["LIVING COUNTRY"],dump_dict[key]["LIVING COUNTRY"]) ) 
		else:
			s += add_dog_info( "Living Country: ", dump_dict[key]["LIVING COUNTRY"].replace("data not available", "?") ) 

		#s += add_dog_info( "Living City: ", dump_dict[key]["LIVING CITY"].replace("data not available", "?") ) 

		s+= """</table>"""

		s+= """</td>"""
		s+= """</tr></table><br>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_id.py" method="GET">Enter dog name:<input name="dog_name" type="text" size="20" value='%s'><input type="submit" value="Find dog ID"></form>"""%dog_name

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_breeders.py" method="GET">Enter  breeder: <input name="name" type="text" size="20"><input type="submit" value="Find breeder"></form><br>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/ancestors_stat.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Ancestors statistic"></form>"""%id

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/offsprings_stat.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Offsprings statistic"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="8">generations<input type="submit" value="Influence statistic  "></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence_inbreed.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="8">generations<input type="submit" value="Influence inbreed  "></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1]"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi_fa.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1 * (1+Fa)]"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/avk.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Ancestor-Loss coefficient"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/rc.py" method="GET">Enter dog1 ID:<input name="dog_id1" type="text" size="5" value=%s>Enter dog2 ID:<input name="dog_id2" type="text" size="5">statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Coefficient of relationship"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/wolf_blood.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s><input type="submit" value="Wolf blood"></form><br>"""%id

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/mk.py" method="GET">Find dogs mean kinship, display first <input name="limit" type="text" size="4" value=1000>dogs<input type="submit" value="Display matching dogs"></form><br>"""
				
		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/group.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s><input type="submit" value="CZ breeding groups"></form>"""%id
		
		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/group_create.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>ID to check in pedigree: <input name="id_to_check" type="text" size="4"><input type="submit" value="Is in pedigree"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/new_groups.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>IDs to check in pedigree: <textarea name="dog_list" rows="4" cols="30">891,938,929,922,930,876,886,885,796,746,744,914,846,924,912</textarea>sorted:<INPUT type=checkbox name="sorted" value="True"><input type="submit" value="Breeding groups"></form><br>"""%id
		
		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_boni.py" method="GET">Enter expression to find in bonitation:<input name="expr" type="text" size="20">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form>"""




		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_training.py" method="GET">Enter expression to find in training:  <input name="expr" type="text" size="20">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form><br>"""



		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_hd.py" method="GET">Find dogs with HD: <TD class="list"><select size="1" name="hd"><option value="A">A</option><option value="B">B</option><option value="C">C</option><option value="D">D</option><option value="E">E</option></select></TD>

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_ed.py" method="GET">Find dogs with ED: <TD class="list"><select size="1" name="ed"><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></TD>

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form>"""



		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_pra.py" method="GET">Find dogs with PRA: <TD class="list"><select size="1" name="pra"><option value="free">free</option><option value="non free">non free</option></select></TD>

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form><br>"""



		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/living_country.py" method="GET">Find dogs living in country: <TD class="list"><select size="1" name="country">

<option value="Albania">Albania</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Bulgaria">Bulgaria</option>
<option value="Canada">Canada</option>
<option value="Croatia">Croatia</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="French Guiana">French Guiana</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Greece">Greece</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Latva">Latva</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Madagascar">Madagascar</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Russia">Russia</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="South Africa">South Africa</option>
<option value="Spain">Spain</option>
<option value="Sweden">Sweden</option>
<option value="Switzerland">Switzerland</option>
<option value="Turkey">Turkey</option>
<option value="Ukraina">Ukraina</option>
<option value="United States">United States</option>
<option value="data not available">?</option>
</select></TD><input type="submit" value="Display matching dogs"></form>"""


		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/living_city.py" method="GET">Find dogs living in city: <input name="city" type="text" size="17"><input type="submit" value="Display matching dogs"></form><br>"""


		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_birth.py" method="GET">Find dogs born in year:<input name="year" type="text" size="4">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD><input type="submit" value="Display matching dogs"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_birth_excel.py" method="GET">Find dogs born in year (EXCEL):<input name="year" type="text" size="4">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD><input type="submit" value="GO"></form><br>"""


		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/nb_offsprings.py" method="GET">Display dogs born after year: <input name="from_year" type="text" size="4"> with more than:<input name="limit" type="text" size="3">offsprings, on <input name="depth" type="text" size="1">generation(s)<input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/consanguinity.py" method="GET">Display dogs with highest COI, born after year: <input name="from_year" type="text" size="4"> display first<input name="limit" type="text" size="3">dogs<input type="submit" value="Display matching dogs"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/avknity.py" method="GET">Display dogs with lowest AVK, born after year: <input name="from_year" type="text" size="4"> display first<input name="limit" type="text" size="3">dogs<input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/no_lejdy.py" method="GET">Dogs born after 1995 with no Lejdy blood. Offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display dogs"></form>"""

	else:
		s = """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_id.py" method="GET">Enter dog name:<input name="dog_name" type="text" size="20"><input type="submit" value="Find dog ID"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_breeders.py" method="GET">Enter  breeder:<input name="name" type="text" size="20"><input type="submit" value="Find breeder"></form><br>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/ancestors_stat.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size=1">generations<input type="submit" value="Ancestors statistic"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/offsprings_stat.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Offsprings statistic"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Influence statistic "></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence_inbreed.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Influence inbreed  "></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1]"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi_fa.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1 * (1+Fa)]"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/avk.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Ancestor-Loss coefficient"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/rc.py" method="GET">Enter dog1 ID:<input name="dog_id1" type="text" size="5">Enter dog2 ID:<input name="dog_id2" type="text" size="5">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Coefficient of relationship"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/wolf_blood.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10"><input type="submit" value="Wolf blood"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/mk.py" method="GET">Find dogs mean kinship, display first <input name="limit" type="text" size="4" value=1000>dogs<input type="submit" value="Display matching dogs"></form><br>"""
				
		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/group.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10"><input type="submit" value="CZ breeding groups"></form>"""
		
		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/group_create.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">ID to check in pedigree: <input name="id_to_check" type="text" size="4"><input type="submit" value="Is in pedigree"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/new_groups.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">IDs to check in pedigree: <textarea name="dog_list" rows="4" cols="30">891,938,929,922,930,876,886,885,796,746,744,914,846,924,912</textarea>sorted:<INPUT type=checkbox name="sorted" value="True"><input type="submit" value="Breeding groups"></form><br>"""
		
		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_boni.py" method="GET">Enter expression to find in bonitation:<input name="expr" type="text" size="20">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_training.py" method="GET">Enter expression to find in training:  <input name="expr" type="text" size="20">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form><br>"""


		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_hd.py" method="GET">Find dogs with HD: <TD class="list"><select size="1" name="hd"><option value="A">A</option><option value="B">B</option><option value="C">C</option><option value="D">D</option><option value="E">E</option></select></TD>

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form>"""



		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_ed.py" method="GET">Find dogs with ED: <TD class="list"><select size="1" name="ed"><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></TD>

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form>"""



		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_pra.py" method="GET">Find dogs with PRA: <TD class="list"><select size="1" name="pra"><option value="free">free</option><option value="non free">non free</option></select></TD>

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form><br>"""



		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/living_country.py" method="GET">Find dogs living in country: <TD class="list"><select size="1" name="country">

<option value="Albania">Albania</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Bulgaria">Bulgaria</option>
<option value="Canada">Canada</option>
<option value="Croatia">Croatia</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="French Guiana">French Guiana</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Greece">Greece</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Latva">Latva</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Madagascar">Madagascar</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Russia">Russia</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="South Africa">South Africa</option>
<option value="Spain">Spain</option>
<option value="Sweden">Sweden</option>
<option value="Switzerland">Switzerland</option>
<option value="Turkey">Turkey</option>
<option value="Ukraina">Ukraina</option>
<option value="United States">United States</option>
<option value="data not available">?</option>
</select></TD><input type="submit" value="Display matching dogs"></form>"""


		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/living_city.py" method="GET">Find dogs living in city: <input name="city" type="text" size="17"><input type="submit" value="Display matching dogs"></form><br>"""


		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_birth.py" method="GET">Find dogs born in year:<input name="year" type="text" size="4">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD><input type="submit" value="Display matching dogs"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_birth_excel.py" method="GET">Find dogs born in year (EXCEL):<input name="year" type="text" size="4">

<select size="1" name="country">
<option value="All Countries">All Countries</option>
<option value="Austria">Austria</option>
<option value="Belgien">Belgien</option>
<option value="Brazil">Brazil</option>
<option value="Canada">Canada</option>
<option value="Czech Republic">Czech Republic</option>
<option value="Denmark">Denmark</option>
<option value="Estonia">Estonia</option>
<option value="Finland">Finland</option>
<option value="France">France</option>
<option value="Germany">Germany</option>
<option value="Great Britan">Great Britan</option>
<option value="Holland">Holland</option>
<option value="Hungary">Hungary</option>
<option value="Italia">Italia</option>
<option value="Izrael">Izrael</option>
<option value="Lithua">Lithua</option>
<option value="Luxemburg">Luxemburg</option>
<option value="Poland">Poland</option>
<option value="Portugal">Portugal</option>
<option value="Romania">Romania</option>
<option value="Slovakia">Slovakia</option>
<option value="Slovenia">Slovenia</option>
<option value="Spain">Spain</option>
<option value="Switzerland">Switzerland</option>
<option value="Ukraina">Ukraina</option>
</select></TD><input type="submit" value="GO"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/nb_offsprings.py" method="GET">Display dogs born after year: <input name="from_year" type="text" size="4"> with more than:<input name="limit" type="text" size="3">offsprings, on <input name="depth" type="text" size="1">generation(s)<input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/consanguinity.py" method="GET">Display dogs with highest COI, born after year: <input name="from_year" type="text" size="4"> display first<input name="limit" type="text" size="3">dogs<input type="submit" value="Display matching dogs"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/avknity.py" method="GET">Display dogs with lowest AVK, born after year: <input name="from_year" type="text" size="4"> display first<input name="limit" type="text" size="3">dogs<input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/no_lejdy.py" method="GET">Dogs born after 1995 with no Lejdy blood. Offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display dogs"></form>"""

	return s



try:
	form = cgi.FieldStorage()
	if form.has_key("id"):
		id = form["id"].value
		s = form_print(id)
	else:
		s= form_print()

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>csv stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/marbre.jpg'>"""
	print """<font face="Arial"><center><h2><b>Statistics on the Czechoslovakian Wolfdogs breed</b></h2></center></font>"""
	print """<center><h6>Help page: <a href=http://www.amicale-chien-loup-tchecoslovaque.com/csvstat.html>HELP</a><h6></center>"""	
	print """<hr>"""
	print """<br>"""
	print """%s"""%s
	print """<h6><p align="right">Database Copyright  www.wolfdog.org</p></h6>"""
	print """<hr>"""
	print """</body></html>"""


except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in form: %s"%e

