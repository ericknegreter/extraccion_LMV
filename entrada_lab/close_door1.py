import RPi.GPIO as GPIO
import time
import os
import mysql.connector
from mysql.connector import Error
import subprocess, datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.IN)
GPIO.setup(22, GPIO.OUT)

#test host
hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost = ('10.0.5.246')

count = 0
opn = 0

def ping(host):
    ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))
    return ret == 0

def net_is_up():
    print ("[%s] Checking if network is up..." % str(datetime.datetime.now()))
    
    xstatus = 1
    for h in hosts:
        if ping(h):
            if ping(localhost):
                print ("[%s] Network is up!" % str(datetime.datetime.now()))
                xstatus = 0
                break
        
    if xstatus:
        time.sleep(10)
        print ("[%s] Network is down :(" % str(datetime.datetime.now())) 
        time.sleep(25)
    
    return xstatus

try:
    while True:
        if GPIO.input(20): # if port 22 == 1
            count+=1
            if count == 15:
                print("the door is open")
                time.sleep(2)
                GPIO.outPut(22, False)
                opn = 0
            time.sleep(2)
        else:
            if opn == 0:
                print("The door was open and now is closed")
                #GPIO.output(22, False)
                while True:
                    if(net_is_up() == 0):
                        #Connection to database LMV and update record in r_muestras table with mysql
                        mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="LABORATORIOT4", database="LMV")
                        mycursor = mydb.cursor()
                        sql = "UPDATE e_extraccion SET estado = 0 WHERE dispositivo='puerta'"
                        mycursor.execute(sql)
                        mydb.commit()
                        print(mycursor.rowcount, "record affected.")
                        time.sleep(1)
                        #END of mysql
                        break
                opn = 1
            print("door is closed")
            count = 0
            time.sleep(1)
finally:                   # this block will run no matter how the try block exits
    GPIO.cleanup()
