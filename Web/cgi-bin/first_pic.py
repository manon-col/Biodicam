#! /usr/bin/python
#-*- coding: utf-8 -*-

import os
from subprocess import check_output

ip_biodicam = check_output(['hostname', '-I'])[0:-2]

print("Content-Type: text/html; charset=utf-8\n\n")         

fichier2 = open("picture_num.txt", "w")
fichier2.write("1")
fichier2.close()	
	
os.system('python display_page.py')