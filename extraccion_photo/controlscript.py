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
from mysql.connector import Error

#Turn on/off LEDS
import RPi.GPIO as GPIO

#Library to read CSV
import csv
import json

#Libary to export image using ssh
import paramiko

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost=('10.0.5.246')
proxy = None

with open('/home/pi/Documents/extraccion_photo/seg.json', 'r', encoding='utf-8') as json_data:
    vrb = json.load(json_data)

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
                print("[%s] Network is up!" % str(datetime.datetime.now()))
                xstatus = 1
                break

    if not xstatus:
        time.sleep(10)
        print("[%s] Network is down :(" % str(datetime.datetime.now()))
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
        if(net_is_up()):
            try:
                #Connection and insert with mysql complete
                mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="MINIMOT4", database="LMV")
                mycursor = mydb.cursor()
                sql = "INSERT INTO imagespath (path, name, person) VALUES (%s, %s, %s)"
                val = (path, name, person)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted")
                mydb.close()
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
    while True:
        if(net_is_up()):
            try:
                #Almacena la imagen en un directorio del servidor para mostrar en pantalla
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect('10.0.5.246', port=19930, username='lmv-codedata', password='Laboratorio', sock=proxy)
                ftp_client = client.open_sftp()
                ftp_client.put(photoname, '/var/www/html/ENTRADA-LMV/Images_Access/'+photoname)
                ftp_client.close()
                break
            except paramiko.AuthenticationException as err:
                print("Fallo en la autentificacion, verifica tus credenciales por favor")
            except paramiko.BadAuthenticationType:
                print("ERROR")
            except paramiko.BadHostKeyException:
                print("Incapaz de verificar claves del host del servidor")
            except paramiko.ChannelException:
                print("ERROR")
            except paramiko.PartialAuthentication as er:
                print("ERROR")
            except paramiko.PasswordRequiredException:
                print("ERROR")
            except paramiko.ProxyCommandFailure:
                print("ERROR")
            except paramiko.SSHException:
                print("Incapaz de establecer conexion ssh")
            finally:
                ftp_client.close()

def security_name(name, spc):
    n = name.lower()
    for x in range(0,7):
        for pat in vrb['permisos'][x]['persona']:
            if pat == n:
                if spc == vrb['permisos'][x]['id']:
                    return True, vrb['permisos'][x]['name']
    return False, "Usuario o contraseña incorrectos"

def take_photo(name, id_):
    validacion, comprobacion = security_name(name, id_)
    if validacion:
        script_dir = os.path.dirname(__file__)
        direc = os.path.dirname(os.path.abspath(__file__))
        os.system('./webcam.sh')
        currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        real_path = currentdate +".jpg"
        abs_file_path = os.path.join(script_dir, real_path)
        GPIO.output(24, False)
        GPIO.output(16, True)
        time.sleep(2)
        store(direc, abs_file_path, comprobacion, real_path)
        GPIO.output(16, False)
        time.sleep(2)
        return False
    else:
        return False

def listen_welcome():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        try:
            print("Adjusting noise")
            r.adjust_for_ambient_noise(source, duration=-1)
            print("Say something!")
            GPIO.output(24, False)
            GPIO.output(12, True)
            print("LISTENED")
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            GPIO.output(12, False)
            GPIO.output(24, True)
            print("Trying to recognize")
            x = r.recognize_google(audio, language="es-mx")
            x = x.split(" ")
            print(x)
            if len(x) != 2:
                return False, "", ""
            idu, nombre, estado = get_name(x)
            #print(frase, nombre, estado)
            if estado == False:
                return False, nombre, idu
            if (idu == "cero" or idu == "uno" or idu == "dos" or idu =="tres" or idu == 'cuatro' or idu == 'cinco'or idu == 'seis'):
                return True, nombre, idu
        except sr.UnknownValueError:
            print("Error trying to understand what you say to me")
            return False, "", ""
        except sr.RequestError as e:
            print("I can't reach google, it's to sad")
            return False, "", ""
        except Exception as e:
            print(e)
            return False, "", ""
        except UnicodeDecodeError:
            return False, "", ""
    return False, "", ""

while True:
    try:
        flag_order = True
        flag_start, nam, id_ = listen_welcome()
        if flag_start:
            while flag_order:
                flag_order = take_photo(nam, id_)
    except ValueError:
        print("Measurement stopped by Error")
    except OSError as err:
        print("OS error: {0}".format(err))
    #except KeyboardInterrupt:
    #    print("Measurement stopped by User")
    #except:
    #    print("Error no controlado")
