#! /usr/bin/python
#-*- coding: utf-8 -*-


import json
import os

print("Content-Type: text/html; charset=utf-8\n\n")     

file = open('/var/www/cgi-bin/cam_infos.json', 'r')
data = json.load(file)
file.close()

data['cam_state'] = 'timelapse'
# resets parameters
data['estimated_nb_pics'] = 0
data['estimated_size'] = 0.0

file = open('/var/www/cgi-bin/cam_infos.json', 'w')
json.dump(data, file)
file.close()

os.system('python display_page.py')