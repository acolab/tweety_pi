# coding: utf-8

import RPi.GPIO as GPIO
import time
import os
import random
from twitter import *
import datetime
import yaml
import sys

pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

with open(sys.argv[1], 'r') as stream:
	keys = yaml.load(stream)

t = Twitter(auth=OAuth(keys["token"], keys["token_secret"], keys["consumer_key"], keys["consumer_secret"]))

time.sleep(30)
now = datetime.datetime.now()
t.statuses.update(status="L'ACoLab est ouvert ! " + now.strftime("%d/%m %Hh%M") + ". N'hésitez pas à passer nous voir.")

print("Ready")
while True:
    input_state = GPIO.input(pin)
    if input_state == False:
	t = Twitter(auth=OAuth(keys["token"], keys["token_secret"], keys["consumer_key"], keys["consumer_secret"]))
	now = datetime.datetime.now()
	t.statuses.update(status="L'ACoLab c'est fini pour aujourd'hui " + now.strftime("%d/%m %Hh%M") +". On se retrouve la prochaine fois.")
        os.system("sudo shutdown -h now")
        exit(0)
    time.sleep(0.2)

