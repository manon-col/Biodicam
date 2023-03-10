# Functional script that scans low resolution images
# and records a burst of images when the difference between
# two consecutive images exceeds a certain threshold.

import time
import picamera
from threading import Thread
from datetime import timedelta

WIDTH = 1920      # Horizontal resolution of recorded pics
HEIGHT =1088     # Vertical resolution of recorded pics
# FPS = 12          # Camera frame rate
CHECK_INTERVAL = 1 # Interval of time (in sec.) between cam status checking

cam_state = "--"

camera = picamera.PiCamera()
camera.resolution = (WIDTH, HEIGHT)
# camera.framerate = FPS

class check_status(Thread):
    
    def __init__(self,time_interval):
        Thread.__init__(self)
        self.time_interval =  time_interval
        self.last_check = time.time() 
        
    def run(self):
        global cam_state
                        
        cam_state = "running"
        
        print("Thread running...")
        
        fichier = open("/var/www/cgi-bin/cam_state.txt", "r")
        cam_state = fichier.read()
        fichier.close()
        
        while True:
            now = time.time()
            if now - self.last_check > self.time_interval:
                self.last_check = now
                fichier = open("/var/www/cgi-bin/cam_state.txt", "r")
                cam_state = fichier.read()
                fichier.close()
                                

def record(interval):
    global lastPic_time
    time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    filename = "/var/www/html/img/biodicam/" + time_stamp + ".jpg"
    camera.capture(filename)
    lastPic_time = now
    time.sleep(interval)


# Camera warm-up time
time.sleep(2)

now = time.time()
lastPic_time = now

thread_statusCheck = check_status(CHECK_INTERVAL)
thread_statusCheck.start()


while True:
    if cam_state == "record":
        
        # Check timelapse state
        fichier = open("/var/www/cgi-bin/timelapse_state.txt", "r")
        timelapse_state = fichier.read()
        fichier.close()
        
        if timelapse_state == "on":
                        
            # Heure actuelle
            current_hour = int(time.strftime("%H", time.localtime()))
            
            # Lecture de la duree totale du timelapse (heures, pauses incluses)
            fichier = open("/var/www/cgi-bin/duration.txt", "r")
            total_duration = timedelta(hours=int(fichier.read())).seconds
            fichier.close()
            timelapse_end = time.time()+total_duration
            
            # Lecture de l'intervalle entre 2 photos (secondes)
            fichier = open("/var/www/cgi-bin/interval.txt", "r")
            interval = int(fichier.read())
            fichier.close()
            
            # Lecture de la tranche horaire de prise de vue
            fichier = open("/var/www/cgi-bin/time_range.txt", "r")
            temp = fichier.read().splitlines()
            fichier.close()
            #  1ere ligne du fichier texte = heure de debut
            start = int(temp[0])
            #  2eme ligne = heure de fin
            end = int(temp[1])
            
            # 1er jour (camera jamais arretee)
            first_day = True
            
            # Timelapse en cours tant qu'on n'excede pas la duree totale
            while time.time() < timelapse_end:
                
                # Debut du timelapse si >= heure début tranche horaire
                if current_hour >= start:
                    
                    # On rallume la camera si ce n'est pas le 1er jour
                    if first_day == False:
                        camera = picamera.PiCamera()
                        camera.resolution = (WIDTH, HEIGHT)
                        # camera.framerate = FPS
                        time.sleep(2)     # warm-up
                    
                    # Timelapse dure jusqu'a la fin de la tranche horaire
                    while current_hour < end and time.time() < timelapse_end:
                        record(interval)
                        current_hour = int(time.strftime("%H", time.localtime()))
                        
                    camera.close()
                    first_day = False
                    
                current_hour = int(time.strftime("%H", time.localtime()))