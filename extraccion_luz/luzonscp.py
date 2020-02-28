import mysql.connector
from mysql.connector import Error
import time
import subprocess, datetime
import RPi.GPIO as GPIO
import sys

#Active GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)

hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost = ('10.0.5.246')

#Getting the turn on or turn off
pru = sys.argv
i = pru[1]
print(i)

def ping(host):
    ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))
    return ret == 0

def net_is_up():
    print ("[%s] Checking if local network is up..." % str(datetime.datetime.now()))
    
    xstatus = 0 
    if ping(localhost):
        print ("[%s] Local network is up!" % str(datetime.datetime.now()))
        xstatus = 1
        
    if xstatus:
        time.sleep(10)
        print ("[%s] Local network is down :(" % str(datetime.datetime.now()))
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
    
            if i == '1':
                if estado == 0:
                    GPIO.output(26, False)
                    #e_extraccion/ Update the register of the e_extraccion table 
                    #Update record in the e_extraccion table of LMV databases
                    sql = "UPDATE e_extraccion SET estado = 1 WHERE dispositivo='luz'"
                    mycursor.execute(sql)
                    mydb.commit()
                    print(mycursor.rowcount, "record affected.")
                    #END of mysql
            elif i == '0':
                if estado == 1:
                    GPIO.output(26, True)
                    #Update the record of the e_extraccion table in LMV databases
                    sql = "UPDATE e_extraccion SET estado = 0 WHERE dispositivo='luz'"
                    mycursor.execute(sql)
                    mydb.commit()
                    print(mycursor.rowcount, "record affected.")
                    #END of mysql
            mydb.close()
            break
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
