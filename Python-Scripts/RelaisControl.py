#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:10:53 2019

@author: mattl
"""

########################################################################################
########################################################################################
def GPIO_init():
    #Initialisierung
    #print("GPIO 21-24 wird als OUT Channel initialisiert")
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)    
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)    
    time.sleep(1)
    #print("GPIO 21-24 erfolgreich initialisiert")

def GPIO_broom():
    #Kanaele aufraeumen    
    #print("GPIO 21-24 werden freigegeben")
    GPIO.cleanup()
    #print("GPIO 21-24 erfolgreich freigegeben")

########################################################################################
########################################################################################
# main program starts here

import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Startmeldung
#print(sys.argv[0]+" wurde aufgerufen")

#falls kein Parameter übergeben wurde, ist die Anzahl der Elemwnte in der Liste 1
if len(sys.argv) == 1: 
    print("Keinen Parameter übergeben !")
    print("Gültige Parameter:")
    print("     >connect< >> alle Relais werden geschlossen")
    print("     >disconnect< >> alle Relais werden geöffnet")
    
#falls Parameter >folder< übergeben wurde    
elif sys.argv[1] == "connect": 
    GPIO_init()
    print('Relais werden geschlossen')
    GPIO.output(21, GPIO.LOW)
    #time.sleep(0.05)
    GPIO.output(22, GPIO.LOW)
    #time.sleep(0.05)
    GPIO.output(23, GPIO.LOW)
    #time.sleep(0.05)
    GPIO.output(24, GPIO.LOW)
    print('......  erledigt')

elif sys.argv[1] == "disconnect": 
    GPIO_init()
    print('Relais werden geöffnet')
    GPIO.output(21, GPIO.HIGH)
    #time.sleep(0.05)
    GPIO.output(22, GPIO.HIGH)
    #time.sleep(0.05)
    GPIO.output(23, GPIO.HIGH)
    #time.sleep(0.05)
    GPIO.output(24, GPIO.HIGH)
    print('......  erledigt')    
            
#falls irgend ein Parameter übergeben wurde
else: 
    print("Keinen Parameter übergeben !")
    print("Gültige Parameter:")
    print("     >connect< >> alle Relais werden geschlossen")
    print("     >disconnect< >> alle Relais werden geöffnet")
   
    
########################################################################################
########################################################################################
# geparkter code

"""    
keiner    
"""
