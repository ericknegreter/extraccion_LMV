import mysql.connector
from mysql.connector import Error
import os 
import time
import subprocess, datetime
import RPi.GPIO as GPIO

#Active GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)

print( "mensaje inicial antes de la espera")
time.sleep(1) # espera en segundos
print ("mensaje luego de la espera")

hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost = ('10.0.5.246')

def ping(host):
    ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))
    return ret == 0

def net_is_up():
    print ("[%s] Checking if network is up..." % str(datetime.datetime.now()))
    
    xstatus = 0
    for h in hosts:
        if ping(h):
            if ping(localhost):
                print ("[%s] Network is up!" % str(datetime.datetime.now()))
                xstatus = 1
                break
        
    if xstatus:
        time.sleep(10)
        print ("[%s] Network is down :(" % str(datetime.datetime.now()))
        time.sleep(25)
        
    return xstatus

while True:
    if(net_is_up()):
        try:
            mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="MINIMOT4", database="LMV")
            mycursor = mydb.cursor()
            sql = "SELECT estado FROM e_extraccion WHERE dispositivo = 'luz'"
            mycursor.execute(sql)
            records = mycursor.fetchall()
            print(mycursor.rowcount, "record selected")
            for row in records:
                estado = int(row[0])

            if estado == 1:
                GPIO.output(26, False)
            elif estado == 0:
                GPIO.output(26, True)
            mydb.close()
            break
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
