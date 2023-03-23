#! /usr/bin/python
#-*- coding: utf-8 -*-

import os

print("Content-Type: text/html; charset=utf-8\n\n")         

nb_pic = len(os.listdir("/var/www/html/img/biodicam/"))
fichier = open("picture_num.txt", "w")
fichier.write(str(nb_pic))
fichier.close()	
	
os.system('python display_page.py')