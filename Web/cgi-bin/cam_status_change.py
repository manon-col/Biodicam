#! /usr/bin/python
#-*- coding: utf-8 -*-

import cgi
import json
import os

print ("Content-Type: text/html; charset=utf-8\n\n")

form = cgi.FieldStorage()
state = form.keys()[0]
    
file = open('/var/www/cgi-bin/cam_infos.json', 'r')
data = json.load(file)
file.close()

data['cam_state'] = state
file = open('/var/www/cgi-bin/cam_infos.json', 'w')
json.dump(data, file)
file.close()

os.system('python display_page.py')