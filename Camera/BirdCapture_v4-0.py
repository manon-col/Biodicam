# Functional script that records several images for a given period of time,
# and separated by a given interval of time. When timelapse mode is off, it
# records preview images.


import time
import picamera
from threading import Thread
from datetime import timedelta


WIDTH = 1920         # Horizontal resolution of recorded pics
HEIGHT =1088         # Vertical resolution of recorded pics
CHECK_INTERVAL = 1   # Interval of time (in sec.) between cam status checking

cam_state = ''
timelapse_state = ''


class check_status(Thread):
    """Allows to check at regular intervals if the camera is activated by the
    user (stop/record mode), as well as timelapse mode (on/off)"""
    
    def __init__(self,time_interval):
        Thread.__init__(self)
        self.time_interval =  time_interval
        self.last_check = time.time() 
        
    def run(self):
        
        global cam_state
        global timelapse_state
        cam_state = "running"
        timelapse_state = "off"
        
        print("Thread running...")
        
        fichier = open("/var/www/cgi-bin/cam_state.txt", "r")
        cam_state = fichier.read()
        fichier.close()
        
        fichier = open("/var/www/cgi-bin/timelapse_state.txt", "r")
        timelapse_state = fichier.read()
        fichier.close()
        
        while True:
            
            now = time.time()
            if now - self.last_check > self.time_interval:
                self.last_check = now
                
                fichier = open("/var/www/cgi-bin/cam_state.txt", "r")
                cam_state = fichier.read()
                fichier.close()
                
                fichier = open("/var/www/cgi-bin/timelapse_state.txt", "r")
                timelapse_state = fichier.read()
                fichier.close()
                                

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
    """Function that reads all timelapse parameters stored in text files"""
    
    # Reading the total timelapse duration (hours, pauses included)
    fichier = open("/var/www/cgi-bin/duration.txt", "r")
    total_duration = timedelta(hours=int(fichier.read())).seconds
    fichier.close()
    timelapse_end = time.time() + total_duration
    
    # Reading the interval between 2 pics (in seconds)
    fichier = open("/var/www/cgi-bin/interval.txt", "r")
    interval = int(fichier.read())
    fichier.close()
    
    # Reading the time range of the recording
    fichier = open("/var/www/cgi-bin/time_range.txt", "r")
    temp = fichier.read().splitlines()
    fichier.close()
    #  1st line of the text file = start time (hour)
    range_start = int(temp[0])
    #  2nd line = end
    range_end = int(temp[1])
    
    params = {"timelapse_end":timelapse_end, "interval":interval,
              "range_start":range_start, "range_end":range_end}
    
    return params


#### Camera management loop ####


thread_statusCheck = check_status(CHECK_INTERVAL)
thread_statusCheck.start()
cam_closed = True  # real state of the picamera
get_params = False  # True only when timelapse params are read


while True:

    if cam_state == "record":
        
        if timelapse_state == "on":
            current_hour = int(time.strftime("%H", time.localtime()))
            
            if get_params == False:
                # 1st time: we fetch the timelapse params
                params = get_timelapse_params()
                timelapse_end = params["timelapse_end"]
                interval = params["interval"]
                range_start = params["range_start"]
                range_end = params["range_end"]
                get_params = True
            
            if (current_hour >= range_start and current_hour < range_end and
                time.time() < timelapse_end):
                
                # Reactivate the camera when in time range
                if cam_closed:
                    camera = picamera.PiCamera()
                    camera.resolution = (WIDTH, HEIGHT)
                    time.sleep(2)     # warm-up time
                    print("Camera activated")
                    cam_closed = False
                record(preview=False, pause=interval)
            
            # Camera stopped at night (or at the very end of timelapse)
            if current_hour >= range_end or current_hour >= timelapse_end:
                camera.close()
                print("Camera stopped")
                cam_closed = True
                
            # End of timelapse
            if time.time() >= timelapse_end:
                fichier = open("/var/www/cgi-bin/cam_state.txt", "w")
                fichier.write("stop")
                fichier.close()
                fichier = open("/var/www/cgi-bin/timelapse_state.txt", "w")
                fichier.write("off")
                fichier.close()
                get_params = False
        
        # Out of timelapse, record a "preview" pic updated every 2 sec
        else:
            get_params = False
            if cam_closed:
                camera = picamera.PiCamera()
                camera.resolution = (WIDTH, HEIGHT)
                time.sleep(2)     # warm-up time
                print("Camera activated")
                cam_closed = False
            record(preview=True, pause=2)
    
    elif cam_closed == False:
        camera.close()
        print("Camera stopped")
        cam_closed = True
        get_params = False