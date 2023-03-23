#! /usr/bin/python

import os
import cgi

print "Content-Type: text/html; charset=utf-8\n\n"

form = cgi.FieldStorage()

duration = form.value("duration")
start_range = form.value("start")
end_range = form.value("end")
interval = form.value("interval")

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