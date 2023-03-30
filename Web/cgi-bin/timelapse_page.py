#! /usr/bin/python
#-*- coding: utf-8 -*-


import json
import os
import socket
from subprocess import check_output

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

# Get size of all images in the file
path = "/var/www/html/img/biodicam"

directory_size = 0
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    directory_size += os.path.getsize(file_path)

BytesPerMB = 1024 * 1024
directory_size = float(directory_size/BytesPerMB)

# reads the estimated size (storage, + number of images) of the timelapse,
# calculated with the chosen parameters
file = open('cam_infos.json', 'r')
data = json.load(file)
nb_pics = data['estimated_nb_pics']
timelapse_size = data['estimated_size']
file.close()


print """

<html>
<head>
 	<title>Sélection des données à afficher</title>
 	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
 	<link rel="icon" type="image/png" href="img/econect-favicon.png" />
     
    <style>
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

    h2 {
        text-align: center;
        font-size: 4em;
    	line-height: 0.4em;
    	color: #1f497d;
    	font-family: Arial;
    	font-weight: bold;
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


<div id="section" style = "top: 330px; font-size: 2em;">

    <td>
Espace de stockage utilisé : 
"""

print(directory_size)

print """
    MB
    </td>
</div>

<div id="section" style = "top: 500px;">
    <table>
    <form id="formulaire" method="post" action="/cgi-bin/timelapse_params.py">
    
        <div style="margin-bottom: 10px; font-size:2em;">
            <label>Durée totale du timelapse (en heures, pauses incluses) :</label>
            <input type="number" name="duration">
        </div>
        <br>
        
        <div style="margin-bottom: 10px; font-size:2em;">
            <label>Début de la tranche horaire (heure, ex : 8) :</label>
            <input type="number" name="start">
        </div>
        <br>
        
        <div style="margin-bottom: 10px; font-size:2em;">
            <label>Fin de la tranche horaire (ex : 18) :</label>
            <input type="number" name="end">
        </div>
        <br>
        
        <div style="margin-bottom: 20px; font-size:2em;">
            <label>Intervalle entre 2 images (en secondes) :</label>
            <input type="number" name="interval">
        </div>
        <br>
        
        <div class="button">
            <button type="submit" id="send_button" style="width: 500px;">Paramétrer</button>
        </div>
        
    </form>
</table>
</div>

<div id="section" style="top: 1000px; font-size:2em;">
    <tr>
    
        <td>
        Estimation du nombre de photos à prendre selon les paramètres entrés :
"""
print(nb_pics)

print """
        <br>
        Estimation de l'espace de stockage nécessaire selon les paramètres entrés : 
"""
print(timelapse_size)
print """
          MB
        <br><br>
        Note : les estimations sont significatives pour une durée de timelapse > 24h.
        </td>
        
    </tr>
</div>

<div id="section" style = "top: 1400px;">

    <table>
    <form id="formulaire" action="/cgi-bin/timelapse_launch.py" method="post" accept-charset="utf-8" lang="fr" >
    <input type="submit" name="launch" value="Lancer le timelapse" id= "send_button" style="width: 700px;">
    </form>
    </table>
    
</div>
"""

print """


<!-- *********************************AUTRES ELEMENTS DE LA PAGE************************************** !-->


<div id="footer">
 	Copyright © Econect
</div>
 
</body>
</html>
"""