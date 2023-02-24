#! /usr/bin/python
#-*- coding: utf-8 -*-

import socket
import os
from subprocess import check_output

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

hostname = socket.gethostname()
ip_biodicam = get_ip()

#ip_biodicam = check_output(['hostname', '-I'])[0:-2] # ne fonctionne que quand connect� au Wifi (en plus du point d'acc�s)
#ip_biodicam = "192.168.167.238" # IP sujette � modification

print("Content-Type: text/html; charset=utf-8\n\n")         

fichier = open("cam_state.txt", "r")
state = fichier.read()
fichier.close()

if state == "record":
	cam_status = "Camera recording..." 
else:
	cam_status = "Camera stopped!"


# Lecture du n� d'image � afficher
fichier2 = open("picture_num.txt", "r")
pic_num = int(fichier2.read())
fichier2.close()

source_dir = "/var/www/html/img/biodicam/"
os.chdir(source_dir)
file_names = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
os.chdir("/var/www/cgi-bin/")

if pic_num > len(file_names):
	pic_num = len(file_names)
	fichier2 = open("picture_num.txt", "w")
	fichier2.write(str(len(file_names)))
	fichier2.close()
	
if pic_num < 1:
	pic_num = 1
	fichier2 = open("picture_num.txt", "w")
	fichier2.write("1")
	fichier2.close()	
		
#file_path = "http://"+ ip_biodicam + "/img/biodicam/" + file_names[-1]
file_path = "http://"+ ip_biodicam + "/img/biodicam/" + file_names[pic_num-1]

file_name_disp = file_names[pic_num-1]

print '''
<head>
	<title>S�lection des donn�es � afficher</title>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<link rel="stylesheet" href="style.css" />
	<link rel="icon" type="image/png" href="img/econect-favicon.png" />
	
	<style>

/* Pour info, codes couleurs utilis�s :
Bleu super fonc� : #333A40
Bleu roy : #1f497d
Bleu clair moyen : #729EBF
Bleu tr�s clair : #E6EBFF

*/

body {
    font-size: 100%;
	background-color:#E6EBFF;
}





#toto { 

}
  

#header_t {
    background-color:#F5DA81;
    color:white;
    text-align:center;
    padding:0px;
	top:0px;
	left:0px;
	font-family: Arial;
	position: fixed;
	width: 100%;
	height:260px;
	z-index: 2000;
	transform: scale(1); 
}





#section {
	width: 90%; 
	margin-left: auto;
	margin-right: auto;
	top: 260px;
	position: absolute; /* absolute � l'origine */
	background-color:;
	height: 500px; /* auto � l'origine */
    padding:2%;	
	font-family: Arial;
	font-size: 1em;
	text-align: justify;
	line-height:1em;
	transform: scale(1); 
}

#section-monitoring {
	width: 100%; 
	margin-left: auto;
	margin-right: auto;
	top: 17px;
	left: -10px;
	position: absolute;
	background-color:;
	height: auto;
    padding:0;	
	font-family: Arial;
	font-size: 1em;
	text-align: justify;
	line-height:1.2em;
	transform: scale(1); 
}

#footer {
    background-color:#F5DA81;
	position: fixed;
	bottom: 0px;
	left: 0px;
	width: 100%;
	height: 75px;
    color:white;
    clear:both;
    text-align:center;
	vertical-align:15px; 
	padding:10px;
	position: fixed;   
	font-family: Arial;
	font-size: 3em;
	z-index: 1995;
	transform: scale(1); 
}

#back_menu {
    background-color:white;
	position: fixed;
	bottom: 160px;
	left: 0px;
	width: 100%;
	height: 250px;
    color:black;
    clear:both;
    text-align:center;
	vertical-align:middle; 
	padding:5px;	 
	position: fixed;   
	font-family: Arial;
	font-size: 2em;
	z-index: 1900;
	transform: scale(1); 
}


#input_field{
	font-size: 6em;
	width: 280px;
	height: 120px;
	border-style: solid;
	border-width: 2px;
	border-color: black;
	padding: 5px;
	text-align: center;
	
}

#select_list{
font-size: 6em;
	width: 380px;
	height: 120px;
	border-style: solid;
	border-width: 1px;
	border-color: black;
	padding: 5px;
	text-align: center;
	color:rgba(0,0,0,0);
	text-shadow: 0 0 0 #000;
}

#radio_button{
    border: 1px;
	border-style: solid;
	font-size: 1.9em;
}

#radio_text{
	font-size: 1.6em;
}


#send_button{
	width: 200px;
	height: 120px;
	border-style: solid;
	border-width: 1px;
	border-color: black;
	font-size: 2em;
	color: white;
	background-color: #DF7401;
	}
	
#send_button:hover {
    background-color: #F7BE81;
	color: white;
	}
	
	
#squ-select{
	position: relative;
	width:80%;
	height:120px;
	background-color: #DF7401;
	color: white;
	border-radius: 10px 10px 10px 10px;
	text-align: center;
	vertical-align: middle;
	line-height: 2.5em;
	font-size: 2.5em;
	/*box-shadow:10px 10px 10px grey;*/
	box-shadow: -1px 2px 5px 1px rgba(0, 0, 0, 0.5), 10px 10px 10px grey; 
	padding: 5%;
	text-decoration-color: #1f497d;
	border-style: none;
	border-width: 0.5px;
	border-color: black;
	}

	
#squ-select:hover {
    background: #F7BE81;
	color: white;
	text-decoration-color: #729EBF;
}



	
#formulaire{
	font-style: normal;
	font-size:0.875em;
	width: 100%;
}



h1{
	text-align: left;
	position: relative;
	font-size: 6em;
	line-height: 0.4em;
	color: #1f497d;
	font-family: Arial;
}

h2 {
    font-size: 1.2em;
	text-align: left;
	line-height: 1.4em;
	font-family: Arial;
}


h3{
	text-align: center;
	font-size: 1em;
	line-height: 0.6em;
	vertical-align: middle;
}

h4{
	text-align: center;
	font-size: 6em;
	line-height: 1.2em;
}

h5{
	text-align: center;
	font-size: 4em;
	line-height: 1.4em;
}

#frame { /* Example size! */
	position : fixed;
	top: 20;
	left: 0;
    height: 500px; /* original height */
    width: 100%; /* original width */
}
#frame {
    height: 500px; /* new height (400 * (1/0.8) ) */
    width: 100%; /* new width (100 * (1/0.8) )*/

    transform: scale(2.5); 
    transform-origin: 0 0;
}


 


</style>

</head>

<body>

<div id="header_t" class="site-header">
	<table id="entete" border=0>
		<tr height=250px>

			<td width=5px>

			</td>
			<td width = 20%>
				<img src = "http://
'''
print(ip_biodicam)

print '''
/img/logo-econect.png" width=250px>
			</td>
			
			<td td width=75%>
				<h1 style="text-align: center; top: 30px; font-size: 1.4 em; color: #B45F04; line-height:1; font-weight: bold;">BiodiCam</h1>
			</td>

		</tr>
	</table>
</div>



<!-- *****************************TEXTE A MODIFIER********************************** !-->

<div id="section" style="text-align: center; top: 370px;">
<br><br><br>
<table style="margin: 0 auto;">

<tr>
'''
if state == "record":
	print '''
	<td>
	<form id="formulaire" action="/cgi-bin/cam_status_change.py" Method="post" accept-charset="utf-8" lang="fr" >
	<input type="submit" name="stop_res" value="Stop" id= "send_button" style="height: 100px; width: 400px; font-size: 4em;";>
	</form>
	</td>
	'''
else:
	print '''
	<td>
	<form id="formulaire" action="/cgi-bin/cam_status_change.py" Method="post" accept-charset="utf-8" lang="fr" >
	<input type="submit" name="stop_res" value="Resume" id= "send_button" style="height: 100px; width: 400px; font-size: 4em;";>
	</form>
	</td>
	'''

print '''

</tr>
</table>

</div>
'''

print """<div><h1 style = "top: 330px; text-align: center;font-size: 4em;">%s</h1>""" % (cam_status)

print("""
<div style = "top: 620px; position: absolute;text-align: center;">
<table style="margin: 0 auto;">
<tr><td>
<img src = "%s" width=950px;>
</td></tr>
<tr><td style = "font-size: 2em;">
%s
</td></tr>
</table>
</div>

""") % (file_path, file_name_disp)

print """
<div style = "top: 1250px; position: absolute; ">
<table>

<tr>
<td width = 2%>
</td>
<td width = 8%>
<form id="formulaire" action="/cgi-bin/first_pic.py" Method="post" accept-charset="utf-8" lang="fr" >
<input type="submit" name="stop_res" value="<<" id= "send_button" style="height: 100px; width: 100px; font-size: 4em;">
</form>
</td>
<td width = 2%>
</td>
<td width = 8%>
<form id="formulaire" action="/cgi-bin/previous_pic.py" Method="post" accept-charset="utf-8" lang="fr" >
<input type="submit" name="stop_res" value="<" id= "send_button" style="height: 100px; width: 100px; font-size: 4em;">
</form>
</td>
<td width>

</td>
<td width = 8%>
<form id="formulaire2" action="/cgi-bin/next_pic.py" Method="post" accept-charset="utf-8" lang="fr" >
<input type="submit" name="preview" value=">" id= "send_button" style="height: 100px; width: 100px; font-size: 4em;">
</form>
</td>
<td width = 2%>
</td>
<td width = 8%>
<form id="formulaire" action="/cgi-bin/last_pic.py" Method="post" accept-charset="utf-8" lang="fr" >
<input type="submit" name="stop_res" value=">>" id= "send_button" style="height: 100px; width: 100px; font-size: 4em;">
</form>
</td>
<td width = 2%>
</td>
</tr>
</table>
</div>
"""

print """



<!-- *********************************AUTRES ELEMENTS DE LA PAGE************************************** !-->







<div id="footer" style="color: #B45F04;">
	Copyright Econect
</div>
 
</body></html>

""" 

