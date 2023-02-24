#! /usr/bin/python
#-*- coding: utf-8 -*-

import os
from subprocess import check_output

#ip_biodicam = check_output(['hostname', '-I'])[0:-2]
#ip_biodicam = "192.168.167.238"

print("Content-Type: text/html; charset=utf-8\n\n")         

fichier = open("cam_state.txt", "r")
state = fichier.read()
fichier.close()

fichier = open("cam_state.txt", "w")
if state == "stop":
	fichier.write("record")
	cam_status = "Camera recording..." 
else:
	fichier.write("stop")
	cam_status = "Camera stopped!"
fichier.close()

os.system('python display_page.py')