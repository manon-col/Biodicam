import time, os        

last_check = time.time()
        
while True:
    now = time.time()
    if now - last_check > 10:
        last_check = now
        fichier = open("/var/www/cgi-bin/reboot.txt", "r")
        reboot_need = fichier.read()
        fichier.close()
        if reboot_need == "yes":
            fichier = open("/var/www/cgi-bin/reboot.txt", "w")
            fichier.write("no")
            fichier.close()
            os.system("sudo reboot")
