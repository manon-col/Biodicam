import time
import picamera
import datetime

# définition des paramètres du timelapse
DURATION = 3600    # Durée du timelapse (1heure)
INTERVAL = 60      # Intervalle entre deux photos
WIDTH = 1920       # Résolution horizontale
HEIGHT = 1088      # Résolution verticale
num_photos = int(DURATION / INTERVAL) #Nombre de photos à capturer dans l'intervalle et avec le pas de temps

camera = picamera.PiCamera()
camera.resolution = (WIDTH, HEIGHT)

# Start time lapse
now = datetime.datetime.now()
for i in range(num_photos):
    time_stamp = now.strftime("%Y%m%d-%H%M%S")
    filename = "/var/www/html/img/biodicam/" + time_stamp + ".jpg"
    camera.capture(filename)
    time.sleep(INTERVAL)
    now += datetime.timedelta(seconds=INTERVAL)

camera.close()