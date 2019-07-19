import Adafruit_DHT
import mysql.connector
import time 
import os 
import subprocess, datetime
import RPi.GPIO as GPIO

# Set sensor tpye: Options are DHT11, DHT22 or AM2301
sensor=Adafruit_DHT.DHT11

#Active GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.OUT)

#Set GPIO sensor is connected to
gpio=17
con = 1

#test host
hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost = ('10.0.5.246')

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
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        if humidity is not None and temperature is not None:
            if temperature > 21.5 and con == 1:
                now = datetime.datetime.now()
                if now.hour >= 8 and now.hour < 18:
                    #os.system('gpio -g mode 27 out')
                    GPIO.output(27, True)
                    time.sleep(1)
                    GPIO.output(27, False)
                    print("encendido")
                    while True:
                        if(net_is_up() == 0):
                            #Connection to database LMV and update record in e_extraccion table with mysql
                            mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="LABORATORIOT4", database="LMV")
                            mycursor = mydb.cursor()
                            sql = "UPDATE e_extraccion SET estado = 1 WHERE dispositivo='aire'"
                            mycursor.execute(sql)
                            mydb.commit()
                            print(mycursor.rowcount, "record affected.")
                            time.sleep(1)
                            #END of mysql
                            break
                con = 2
            elif temperature < 19.5 and con == 2:
                now = datetime.datetime.now()
                if now.hour >= 8 and now.hour < 18:
                    #os.system('gpio -g mode 27 in')
                    GPIO.output(27, True)
                    time.sleep(1)
                    GPIO.output(27, False)
                    print("apagado")
                    while True:
                        if(net_is_up() == 0):
                            #Connection to database LMV and update record in e_extraccion table with mysql
                            mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="LABORATORIOT4", database="LMV")
                            mycursor = mydb.cursor()
                            sql = "UPDATE e_extraccion SET estado = 0 WHERE dispositivo='aire'"
                            mycursor.execute(sql)
                            mydb.commit()
                            print(mycursor.rowcount, "record affected.")
                            time.sleep(1)
                            #END of mysql
                            break
                con = 1
            print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
#Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
