#!/usr/bin/python

print ("Content-type: text/html\n\n")

import os
import cgi

form = cgi.FieldStorage()

duration = form.getvalue("duration")
start_range = form.getvalue("start")
end_range = form.getvalue("end")
interval = form.getvalue("interval")

with open("duration.txt", "w") as fichier :
    fichier.write(duration)
with open("time_range.txt", "w") as fichier :
    fichier.write(f"{start_range}\n{end_range}")
with open("interval", "w") as fichier :
    fichier.write(interval)

with open("cam_state.txt", "w") as fichier :
    fichier.write("record")
with open("timelapse_state.txt", "w") as fichier :
    fichier.write("on")

os.system('python display_page.py')