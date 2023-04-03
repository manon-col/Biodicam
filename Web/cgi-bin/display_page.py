#! /usr/bin/python
#-*- coding: utf-8 -*-


import json
import os
import socket
from subprocess import check_output
import time

print("Content-Type: text/html; charset=utf-8\n\n")         

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

#ip_biodicam = check_output(['hostname', '-I'])[0:-2] # ne fonctionne que quand connecté au Wifi (en plus du point d'accès)
#ip_biodicam = "192.168.167.238" # IP sujette à modification

# Pour éviter de faire crasher le site si la lecture du json a lieu à un moment
# où le fichier est vide
test = True
while test :
    try :
        file = open('cam_infos.json', 'r')
        data = json.load(file)
        state = data['cam_state']
        timelapse_end = data['timelapse_end']
        file.close()
        test = False
    except :
        0 == 0


if state == "preview":
	cam_status = "Preview mode on" 
elif state == "timelapse":
	cam_status = "Timelapse in progress..."
elif state == "pause":
    cam_status = "Timelapse paused..."
elif state == "stop":
    cam_status = "Camera stopped!"


# Lecture du n° d'image à afficher
file = open("picture_num.txt", "r")
pic_num = int(file.read())
file.close()

source_dir = "/var/www/html/img/biodicam/"
os.chdir(source_dir)
file_names = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
os.chdir("/var/www/cgi-bin/")

if pic_num > len(file_names):
	pic_num = len(file_names)
	file = open("picture_num.txt", "w")
	file.write(str(len(file_names)))
	file.close()
	
if pic_num < 1:
	pic_num = 1
	file = open("picture_num.txt", "w")
	file.write("1")
	file.close()	
		
#file_path = "http://"+ ip_biodicam + "/img/biodicam/" + file_names[-1]
file_path = "http://"+ ip_biodicam + "/img/biodicam/" + file_names[pic_num-1]

file_name_disp = file_names[pic_num-1]


print """
<html>
<head>
	<title>Sélection des données à afficher</title>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<link rel="icon" type="image/png" href="img/econect-favicon.png">
    
    <style>
    /* Pour info, codes couleurs utilisés :
    Bleu super foncé : #333A40
    Bleu roy : #1f497d
    Bleu clair moyen : #729EBF
    Bleu très clair : #E6EBFF
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
    	position: absolute; /* absolute à l'origine */
    	background-color:;
    	height: 500px; /* auto à l'origine */
        padding:2%;	
    	font-family: Arial;
    	text-align: center;
    	line-height:1.2em;
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

    #table {
        margin: 0 auto;}

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

    #footer {
        background-color:#F5DA81;
        color: #B45F04
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
        height: 100px;
        border-style: solid;
        border-width: 1px;
        border-color: black;
        font-size: 4em;
        color: white;
        background-color: #DF7401;
    	}
    	
    #send_button:hover {
        background-color: #F7BE81;
        color: white;
    	}
    	
    #formulaire{
        font-style: normal;
        width: 100%;
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

    h1{
        text-align: center;
        position: relative;
    	font-size: 6em;
    	line-height: 1;
    	color: #B45F04;
    	font-family: Arial;
    	font-weight: bold;
    }


    h2{
    	text-align: center;
    	position: relative;
    	font-size: 4em;
    	line-height: 0.4em;
    	color: #1f497d;
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

<div id="header_t">
	<table id="entete" border=0>
		<tr height=250px>
        
			<td width=5px>
			</td>
            
			<td width = 20%>
				<img src = "http://
"""
print(ip_biodicam)

print """
/img/logo-econect.png" width=250px>
			</td>
			
			<td td width=75%>
				<h1 id="h1" style="top: 30px;">BiodiCam</h1>
			</td>
            
		</tr>
	</table>
</div>


<!-- *****************************TEXTE A MODIFIER********************************** !-->


<div id="section" style="top: 370px;">
<br><br><br>
    <table id="table">
    <tr>
    <td>
"""

if state == "stop":
    print '''
    <form id="formulaire" action="/cgi-bin/cam_status_change.py" method="post" accept-charset="utf-8" lang="fr" >
    <input type="submit" name="preview" value="Preview" id= "send_button" style="width: 400px;">
    </form>
    '''

if state == 'preview':
    print '''
    <form id="formulaire" action="/cgi-bin/cam_status_change.py" method="post" accept-charset="utf-8" lang="fr" >
    <input type="submit" name="stop" value="Stop preview" id= "send_button" style="width: 500px;">
    </form>
    '''

if state == "timelapse":
    print '''
    <form id="formulaire" action="/cgi-bin/cam_status_change.py" method="post" accept-charset="utf-8" lang="fr" >
    <input type="submit" name="stop" value="Stop timelapse" id= "send_button" style="width: 500px;">
    </form>
    '''
        

if state == 'pause':
    print '''
    <form id="formulaire" action="/cgi-bin/cam_status_change.py" method="post" accept-charset="utf-8" lang="fr" >
    <input type="submit" name="stop" value="Stop timelapse" id= "send_button" style="width: 500px;">
    </form>
    '''

print '''
    </td>
    </tr>
    </table>
</div>
'''

print """<h2 id="h2"" style = "top: 330px;">%s</h2>""" % (cam_status)

print("""
<div id="section" style="top: 620px;">

    <table id="table">
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
            <form id="formulaire" action="/cgi-bin/first_pic.py" method="post" accept-charset="utf-8" lang="fr" >
            <input type="submit" name="first_pic" value="<<" id= "send_button" style="width: 100px;">
            </form>
            </td>
            
            <td width = 2%>
            </td>
            <td width = 8%>
            <form id="formulaire" action="/cgi-bin/previous_pic.py" method="post" accept-charset="utf-8" lang="fr" >
            <input type="submit" name="previous_pic" value="<" id= "send_button" style="width: 100px;">
            </form>
            </td>

            <td width>
            </td>
            <td width = 8%>
            <form id="formulaire" action="/cgi-bin/next_pic.py" Method="post" accept-charset="utf-8" lang="fr" >
            <input type="submit" name="next_pic" value=">" id= "send_button" style="width: 100px;">
            </form>
            </td>
            
            <td width = 2%>
            </td>
            <td width = 8%>
            <form id="formulaire" action="/cgi-bin/last_pic.py" Method="post" accept-charset="utf-8" lang="fr" >
            <input type="submit" name="last_pic" value=">>" id= "send_button" style="width: 100px;">
            </form>
            </td>
            <td width = 2%>
            </td>
            
        </tr>
    </table>
</div>

<div id="section" style = "top: 1400px;">

    <td>
    <form id="formulaire" action="/cgi-bin/timelapse_page.py" method="post" accept-charset="utf-8" lang="fr" >
    <input type="submit" name="timelapse_page" value="Lancer un timelapse" id= "send_button" style="width: 700px;">
    </form>
    </td>
    
</div>
"""

if state == 'timelapse' or state == 'pause':
    
    remaining_time = int(timelapse_end-time.time())
    days = remaining_time // (24 * 3600)
    remaining_time = remaining_time % (24 * 3600)
    hours = remaining_time // 3600
    remaining_time %= 3600
    minutes = remaining_time // 60
    remaining_time %= 60
    seconds = remaining_time
    
    print'''
    <div id="section" style="top: 1550px; font-size: 2em">
    '''
    print("Temps restant avant la fin du timelapse : {} jour(s), {} heure(s), {} minute(s), {} seconde(s)".format(days, hours, minutes, seconds))
    print'''
    </div>
    '''

print """

<div id="section" style ="top: 1700px">

<td>
<form id="formulaire" action="/cgi-bin/shutdown.py" method="post" accept-charset="utf-8" lang="fr" >
<input type="image" src="http://
"""
print(ip_biodicam)

print """
/img/shutdown.png" alt="Arrêt" width="100px">
</form>
</td>
    
</div>



<!-- *********************************AUTRES ELEMENTS DE LA PAGE************************************** !-->


<div id="footer">
	Copyright © Econect
</div>
 
</body>
</html>
"""