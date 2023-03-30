# Functional script that records several images for a given period of time,
# and separated by a given interval of time. When timelapse mode is off, it
# records preview images.


import json
import picamera
from threading import Thread
import time


WIDTH = 1920         # Horizontal resolution of recorded pics
HEIGHT = 1088         # Vertical resolution of recorded pics
CHECK_INTERVAL = 1   # Interval of time (in sec.) between cam status checking
cam_state = ''

# To be sure that cam state is "stop" when the raspberry pi starts
file = open('/var/www/cgi-bin/cam_infos.json', 'r')
data = json.load(file)
file.close()
data['cam_state'] = 'stop'
file = open('/var/www/cgi-bin/cam_infos.json', 'w')
json.dump(data, file)
file.close()


class check_status(Thread):
    """Allows to check at regular intervals the user-defined camera status"""
    
    def __init__(self,time_interval):
        Thread.__init__(self)
        self.time_interval =  time_interval
        self.last_check = time.time() 
        
    def run(self):
        
        global cam_state
        print("Thread running...")
        
        file = open('/var/www/cgi-bin/cam_infos.json', 'r')
        cam_state = json.load(file)['cam_state']
        file.close()
        
        while True:
            
            now = time.time()
            if now - self.last_check > self.time_interval:
                self.last_check = now
                
                file = open('/var/www/cgi-bin/cam_infos.json', 'r')
                cam_state = json.load(file)['cam_state']
                file.close()


def record(preview, pause):
    """Function that triggers a shot, records the image depending on whether it
    is a preview or not, then realizes the stop time in seconds given as an
    argument"""
    
    global camera
    if preview: filename = "/var/www/html/img/biodicam/preview.jpg"
    else :
        time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        filename = "/var/www/html/img/biodicam/" + time_stamp + ".jpg"
    camera.capture(filename)
    time.sleep(pause)

    
def get_timelapse_params():
    """Function that reads all timelapse parameters stored in the json file"""
    
    file = open('/var/www/cgi-bin/cam_infos.json', 'r')
    params = json.load(file)
    file.close()
    return params


def write_state(state):
    """Function that changes the value of cam_state in the json file"""
    
    global CHECK_INTERVAL
    file = open('/var/www/cgi-bin/cam_infos.json', 'r')
    data = json.load(file)
    file.close()
    data['cam_state'] = state
    file = open('/var/www/cgi-bin/cam_infos.json', 'w')
    json.dump(data, file)
    file.close()
    time.sleep(CHECK_INTERVAL) # to avoid errors with check_status...


#### Camera management loop ####


thread_statusCheck = check_status(CHECK_INTERVAL)
thread_statusCheck.start()
cam_closed = True  # real state of the picamera != the one given by the user
get_params = False  # True only when timelapse parameters are read


while True:
    
    current_hour = int(time.strftime("%H", time.localtime()))

    if cam_state == 'stop': get_params = False
    
    # Part that manages the activation and closure of the picamera, matching the
    # user's instructions to the actual condition of the picamera
    
    if (cam_state == 'preview' or cam_state=='timelapse') and cam_closed:
        camera = picamera.PiCamera()
        camera.resolution = (WIDTH, HEIGHT)
        time.sleep(2)     # warm-up time
        cam_closed = False
        print("Camera is on")
    
    if (cam_state == 'stop' or cam_state == 'pause') and not cam_closed:
        camera.close()
        cam_closed = True
        print("Camera closed")
    
    # Preview mode
    if cam_state == 'preview': record(preview=True, pause=5)
    
    # Timelapse, when not paused (= in the time range)
    if cam_state == 'timelapse':
        
        if get_params == False:
            # At the beginning of the timelapse: fetches its parameters
            params = get_timelapse_params()
            timelapse_end = params['timelapse_end']
            interval = params['interval']
            start_range = params['start_range']
            end_range = params['end_range']
            get_params = True
        
        if (current_hour >= start_range and current_hour < end_range and \
            time.time() < timelapse_end):
            record(preview=False, pause=interval)
            
        # Camera stopped at night
        if current_hour >= end_range :
            write_state('pause')
        
        # End of timelapse
        if time.time() >= timelapse_end:
            write_state('stop')
    
    # When the timelapse is initiated, but paused (ex: at night)
    if cam_state == 'pause':
        
        # Timelapse resumes
        if current_hour >= start_range and current_hour < end_range:
            write_state('timelapse')
        
        # If the timelapse ends during the pause
        if time.time() >= timelapse_end:
            write_state('stop')