#! /usr/bin/python
import cgi, time

try:
	import cPickle as pck
except ImportError:
	import pickle as pck

def form_print(id=0):

	if id !=0:
		f = file("SWHDB", 'rb')
		dump_dict = pck.load(f)
		f.close()

		dog_name = dump_dict[id]["NAME"].replace("'", " ")

		link_str = """<a href=http://www.saarlooswolfdog.com/images/swh/%s.jpg>Pictures of this dog</a><br>"""%dump_dict[id]["REG_NUM"].replace(" ", "%20")

		s = """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_id_saarloos.py" method="GET">Enter dog name:<input name="dog_name" type="text" size="30" value='%s'><input type="submit" value="Find dog ID"> %s</form><br>"""%(dog_name, link_str)

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/ancestors_stat_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Ancestors statistic"></form>"""%id

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/offsprings_stat_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Offsprings statistic"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="6">generations<input type="submit" value="Influence statistic  "></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence_inbreed_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="6">generations<input type="submit" value="Influence inbreed  "></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1]"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi_fa_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1 * (1+Fa)]"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/avk_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s>statistic for:<input name="depth" type="text" size="1" value="5">generations<input type="submit" value="Ancestor-Loss coefficient"></form>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/wolf_blood_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10" value=%s><input type="submit" value="Wolf blood"></form><br>"""%id

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/colors_saarloos.py" method="GET">Find dogs with color: <TD class="list"><select size="1" name="color"><option value="White">White</option><option value="Forest-Brown">Forest-Brown</option><option value="Wolf-gray">Wolf-gray</option></select></TD><input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_hd_saarloos.py" method="GET">Find dogs with HD: <TD class="list"><select size="1" name="hd"><option value="A">A</option><option value="B">B</option><option value="C">C</option><option value="D">D</option><option value="E">E</option></select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_birth_saarloos.py" method="GET">Find dogs born in year:<input name="year" type="text" size="4"><input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/nb_offsprings_saarloos.py" method="GET">Display dogs born after year: <input name="from_year" type="text" size="4"> with more than:<input name="limit" type="text" size="3">offsprings, on <input name="depth" type="text" size="1">generation(s)<input type="submit" value="Display matching dogs"></form>"""

	else:
		s = """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_id_saarloos.py" method="GET">Enter dog name:<input name="dog_name" type="text" size="30"><input type="submit" value="Find dog ID"></form><br>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/ancestors_stat_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size=1">generations<input type="submit" value="Ancestors statistic"></form>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/offsprings_stat_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Offsprings statistic"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Influence statistic "></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/influence_inbreed_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Influence inbreed  "></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1]"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/coi_fa_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Coefficient of inbreeding [Sum (1/2)^n1+n2+1 * (1+Fa)]"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/avk_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10">statistic for:<input name="depth" type="text" size="1">generations<input type="submit" value="Ancestor-Loss coefficient"></form>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/wolf_blood_saarloos.py" method="GET">Enter dog ID:<input name="dog_id" type="text" size="10"><input type="submit" value="Wolf blood"></form><br>"""

		s += """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/colors_saarloos.py" method="GET">Find dogs with color: <TD class="list"><select size="1" name="color"><option value="White">White</option><option value="Forest-Brown">Forest-Brown</option><option value="Wolf-gray">Wolf-gray</option></select></TD><input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_hd_saarloos.py" method="GET">Find dogs with HD: <TD class="list"><select size="1" name="hd"><option value="A">A</option><option value="B">B</option><option value="C">C</option><option value="D">D</option><option value="E">E</option></select></TD>with offsprings:<INPUT type=checkbox name="offspring" value="True"><input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/find_birth_saarloos.py" method="GET">Find dogs born in year:<input name="year" type="text" size="4"><input type="submit" value="Display matching dogs"></form><br>"""

		s +=  """<form action="http://www.amicale-chien-loup-tchecoslovaque.com/cgi-bin/nb_offsprings_saarloos.py" method="GET">Display dogs born after year: <input name="from_year" type="text" size="4"> with more than:<input name="limit" type="text" size="3">offsprings, on <input name="depth" type="text" size="1">generation(s)<input type="submit" value="Display matching dogs"></form>"""

	return s


try:
	form = cgi.FieldStorage()
	if form.has_key("id"):
		id = form["id"].value
		s = form_print(id)
	else:
		s= form_print()

	print "Content-Type: text/html\n"
	print """<html><HEAD><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><TITLE>swh stat</TITLE></HEAD>"""
	print """<body background='http://www.amicale-chien-loup-tchecoslovaque.com/marbre.jpg'>"""
	print """<font face="Arial"><center><h2><b>Statistics on the Saarloos Wolfdog breed</b></h2></center></font>"""
	print """<center><h6>Help page: <a href=http://www.amicale-chien-loup-tchecoslovaque.com/csvstat.html>HELP</a><h6></center>"""	
	print """<hr>"""
	print """<br>"""
	print """%s"""%s

	print """<h6><p align="right">Database Copyright www.saarlooswolfdog.com</p></h6>"""
	print """<hr>"""
	print """</body></html>"""


except Exception, e:
	print "Content-Type: text/html\n"
	print "Error in form: %s"%e

