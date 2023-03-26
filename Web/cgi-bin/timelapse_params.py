#! /usr/bin/python
#-*- coding: utf-8 -*-


import cgi
import datetime
import json
import os
import time

print ("Content-Type: text/html; charset=utf-8\n\n")

form = cgi.FieldStorage()  # gets inputs of the html form (timelapse_page.py)

duration = form["duration"].value
start_range = form["start"].value
end_range = form["end"].value
interval = form["interval"].value


def estimate_result():
    """function that calculate the total number of pictures that would be
    recorded during the timelapse in function of the parameters given by the
    user, then multiplicate it by the estimated size of a picture"""
    
    global duration, start_range, end_range, interval
    duration = int(duration)
    start_range = int(start_range)
    end_range = int(end_range)
    interval = int(interval)
        
    pic_size = 1.5 # estimate of a pic size, in MB
   
    timelapse_start = datetime.datetime.now()  # when timelapse begins
    timelapse_end = timelapse_start + datetime.timedelta(hours=duration)
    diff = timelapse_end - timelapse_start
    day_start = datetime.time(start_range, 0, 0) # start of time range
    day_end = datetime.time(end_range, 0, 0)
    total_time = datetime.timedelta() # counter of straight recording time
    
    for d in range (1, diff.days+1):
    # increments total_time at each recording day
        
        day = timelapse_start + datetime.timedelta(days=d)
        if day.date() == timelapse_start.date():
            record_start = timelapse_start.time()
        else: record_start = day_start
        if day.date() == timelapse_end.date():
            record_end = timelapse_end.time()
        else: record_end = day_end
        if record_end <= record_start: continue
        
        record_start = max(record_start, day_start)
        record_end = min(record_end, day_end)
        total_time += datetime.datetime.combine(datetime.date.min, record_end)\
            - datetime.datetime.combine(datetime.date.min, record_start)
    
    total_seconds = total_time.days*86400 + total_time.seconds
    nb_pics = total_seconds/interval
    
    return nb_pics, nb_pics*pic_size

# additional parameters
estimate = estimate_result()
estimated_nb_pics = estimate[0]
estimated_size = estimate[1]
total_duration = int(duration)*3600
timelapse_end = time.time() + total_duration

# writes all the parameters in the json file
file = open('cam_infos.json', 'r')
data = json.load(file)
file.close()
data['duration'] = duration
data['timelapse_end'] = timelapse_end
data['start_range'] = start_range
data['end_range'] = end_range
data['interval'] = interval
data['estimated_nb_pics'] = estimated_nb_pics
data['estimated_size'] = estimated_size

file = open('cam_infos.json', 'w')
json.dump(data, file)
file.close()

os.system('python timelapse_page.py')