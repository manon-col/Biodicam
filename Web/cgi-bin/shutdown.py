#! /usr/bin/python
#-*- coding: utf-8 -*-

import os

print ("Content-Type: text/html; charset=utf-8\n\n")

sudo_password = 'biodicam'
command = 'sudo shutdown now'

sudo_command = 'echo {} | {} -S {}'.format(sudo_password, 'sudo', command)

os.system(sudo_command)