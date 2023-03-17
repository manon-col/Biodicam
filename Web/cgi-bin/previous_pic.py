#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
from subprocess import check_output

ip_biodicam = check_output(['hostname', '-I'])[0:-2]

print("Content-Type: text/html; charset=utf-8\n\n")         


# Lecture du n° d'image en mémoire
fichier2 = open("picture_num.txt", "r")
pic_num = int(fichier2.read())
fichier2.close()

# Incrémentation du n° d'image
pic_num -= 1
fichier2 = open("picture_num.txt", "w")
fichier2.write(str(pic_num))
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
	
os.system('python display_page.py')