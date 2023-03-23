#! /usr/bin/python
#-*- coding: utf-8 -*-

import os

print("Content-Type: text/html; charset=utf-8\n\n")     

ip_biodicam = '192.168.4.1'

# Get size of all images in the file
path = "/var/www/html/img/biodicam"

directory_size = 0
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    directory_size += os.path.getsize(file_path)

BytesPerMB = 1024 * 1024
directory_size = float(directory_size/BytesPerMB)

f = open("size.txt", "r")
timelapse_size = f.read()
f.close()

print '''
<head>
	<title>Sélection des données à afficher</title>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<link rel="stylesheet" href="style.css" />
	<link rel="icon" type="image/png" href="img/econect-favicon.png" />
	
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
'''

print"""
<!-- *****************************TEXTE A MODIFIER********************************** !-->

<div style = "top: 330px; position: absolute; text-align: center; font-size: 2em;">
<td>
Espace de stockage utilisé : 
"""

print(directory_size)

print """
MB
</td>
</div>

<div style = "top: 500px; position: absolute; text-align: center; font-size: 2em;">
<table>
<form id="formulaire" method="post" action="/cgi-bin/timelapse_params.py">

    <div style="margin-bottom: 10px">
        <label>Durée totale du timelapse (en heures, pauses incluses) :</label>
        <input type="text" name="duration">
    </div>
    <div style="margin-bottom: 10px">
        <label>Début de la tranche horaire (heure, ex : 8) :</label>
        <input type="text" name="start">
    </div>
    <div style="margin-bottom: 10px">
        <label>Fin de la tranche horaire (ex : 18) :</label>
        <input type="text" name="end">
    </div>
    <div style="margin-bottom: 20px;">
        <label>Intervalle entre 2 images (en secondes) :</label>
        <input type="text" name="interval">
    </div>
    <br>
    <div class="button">
        <button type="submit" id="send_button" style="height: 100px; width: 500px;">Paramétrer</button>
    </div>
</form>
</table>
</div>

<div style = "top: 900px; position: absolute; text-align: center; font-size: 2em;">
"""

print """
<tr>
<td>
Estimation de l'espace de stockage nécessaire selon les paramètres entrés : 
"""
print(timelapse_size)
print """
 MB
</td>
<br><br>
<form id="form_launch" action="/cgi-bin/timelapse_launch.py" method="post" accept-charset="utf-8" lang="fr" >
<input type="submit" name="launch" value="Lancer le timelapse" id= "send_button" style="height: 100px; width: 700px; font-size: 2em;";>
</form>
</td>
</tr>

"""

print """
</div>

<!-- *********************************AUTRES ELEMENTS DE LA PAGE************************************** !-->
<div id="footer" style="color: #B45F04;">
	Copyright © Econect
</div>
 
</body>
</html>
"""