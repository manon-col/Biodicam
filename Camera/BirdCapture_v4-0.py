import time
import datetime
import picamera
from threading import Thread

# définition des paramètres du timelapse
DURATION = 3600    # Durée du timelapse (1heure)
INTERVAL = 10      # Intervalle entre deux photos
WIDTH = 1920       # Résolution horizontale
HEIGHT = 1088      # Résolution verticale
num_photos = int(DURATION / INTERVAL) #Nombre de photos à capturer dans l'intervalle et avec le pas de temps

camera = picamera.PiCamera()
camera.resolution = (WIDTH, HEIGHT)

# Initialisation de la variable globale
cam_state = "idle"

class check_status(Thread):
    def __init__(self,time_interval):
        Thread.__init__(self)
        self.time_interval =  time_interval
        self.last_check = time.time()    
    def run(self):
        global cam_state
        cam_state = "running"
        
        print("Thread running...")
        
        while True:
            now = time.time()
            if now - self.last_check > self.time_interval:
                self.last_check = now
                fichier = open("/var/www/cgi-bin/cam_state.txt", "r")
                cam_state = fichier.read().strip()
                fichier.close()


# Start time lapse
info_stop_toDisp = True

thread = check_status(1)
thread.start()

while True:
    if cam_state == "record":
        info_stop_toDisp = True
        ref_time = time.time()
        for i in range(num_photos):
            now = ref_time + i*INTERVAL
            time_stamp = datetime.datetime.fromtimestamp(now).strftime("%Y%m%d-%H%M%S")
            filename = "/var/www/html/img/biodicam/" + time_stamp + ".jpg"
            camera.capture(filename)
            time.sleep(INTERVAL)
    
    else:
        if info_stop_toDisp == True:
            print("Camera stopped")
            info_stop_toDisp = False