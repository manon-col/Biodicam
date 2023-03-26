#! /usr/bin/python
#-*- coding: utf-8 -*-

import os

print("Content-Type: text/html; charset=utf-8\n\n")         

fichier2 = open("picture_num.txt", "w")
fichier2.write("1")
fichier2.close()	
	
os.system('python display_page.py')