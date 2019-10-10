#!/usr/bin/python3.5
#Voice Recognition
import speech_recognition as sr
import os
import unidecode

#Image Capturin
import datetime
import sys
import time
import subprocess

#Store Image
import mysql.connector

#Turn on/off LEDS
import RPi.GPIO as GPIO

#Library to read CSV
import csv

#Libary to export image using ssh
import paramiko

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost=('10.0.5.246')
proxy = None

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

def get_name(Name):
    reader = csv.reader(open("nombres.csv", "rt"), delimiter=",")
    x=list(reader)

    Name2=Name[1]
    Name2=Name2.upper()

    for item in x:
        if str(Name2) == item[0]:
            return Name[0], Name2, True
            break
    return Name[0], "", False

def store(path, name, person, photoname):
    while True:
        if(net_is_up() == 0):
            #Connection and insert with mysql complete
            mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="LABORATORIOT4", database="LMV")
            mycursor = mydb.cursor()
            sql = "INSERT INTO imagespath (path, name, person) VALUES (%s, %s, %s)"
            val = (path, name, person)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted")
            #Almacena la imagen en un directorio del servidor para mostrar en pantalla
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('10.0.5.246', username='lmv-codedata', password='Laboratorio', sock=proxy)
            ftp_client = client.open_sftp()
            ftp_client.put(photoname, '/var/www/html/ENTRADA-LMV/Images_Access/'+photoname)
            ftp_client.close()
            break

def take_photo(name):
    script_dir = os.path.dirname(__file__)
    direc = os.path.dirname(os.path.abspath(__file__))
    os.system('./webcam.sh')
    currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    real_path = currentdate +".jpg"
    abs_file_path = os.path.join(script_dir, real_path)
    GPIO.output(21, False)
    GPIO.output(16, True)
    time.sleep(2)
    #print("--------------------------------------------------")
    #print(direc)
    #print(abs_file_path)
    #print("--------------------------------------------------")
    store(direc, abs_file_path, name, real_path)
    GPIO.output(16, False)
    time.sleep(2)
    return False

def listen_welcome():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        print("Adjusting noise")
        r.adjust_for_ambient_noise(source, duration=-1)
        print("Say something!")
        try:
            GPIO.output(21, False)
            GPIO.output(12, True)
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            GPIO.output(12, False)
            GPIO.output(21, True)
            print("LISTENED")
            print("Trying to recognize")
            x = r.recognize_google(audio, language="es-mx")
            x = x.split(" ")
            #print(x)
            if len(x) != 2:
                return False, ""
            frase, nombre, estado = get_name(x)
            #print(frase, nombre, estado)
            if estado == False:
                return False, nombre
            if (frase=="Okay" or frase=="okay" or frase=="oK" or frase=="OK"  or ("ok" in frase) or ("Ok" in frase)):
                return True, nombre
        except sr.UnknownValueError:
            print("Error trying to understand what you say to me")
            return False, ""
        except sr.RequestError as e:
            print("I can't reach google, it's to sad")
            return False, ""
        except Exception as e:
            print(e)
            return False, ""
        except UnicodeDecodeError:
            return False, ""
    return False, ""

while True:
    try:
        #r = sr.Recognizer()
        #m = sr.Microphone()
        flag_order = True
        flag_start, nam = listen_welcome()
        if flag_start:
            while flag_order:
                flag_order = take_photo(nam)
    except ValueError:
        print("Measurement stopped by Error")
    except OSError as err:
        print("OS error: {0}".format(err))
    #except KeyboardInterrupt:
    #    print("Measurement stopped by User")
