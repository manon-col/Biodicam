#! /usr/bin/python

import cgi
import os

print ("Content-Type: text/html; charset=utf-8\n\n")

state = cgi.FieldStorage()
print(state)

fichier = open("cam_state.txt", "w")
fichier.write(state)
fichier.close()

os.system('python display_page.py')