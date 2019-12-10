echo "Actualizacion de SO"
apt-get update && apt-get upgrade -y
echo "Instalacion de herramientas"
apt-get install vim -y
apt-get install python-pip -y
apt-get install python3-pip -y
apt-get install fswebcam -y
apt-get install git-core -y
apt-get install xterm -y
sudo apt-get install python-dev default-libmysqlclient-dev -y
sudo apt-get install python3-dev
sudo apt-get install python3-mysql.connector
sudo apt-get install flac
sudo apt-get install portaudio19-dev -y
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
apt-get install build-essential python-dev -y 
apt-get install build-essential python3-dev -y 
python3 setup.py install
cd ..
echo "Instalacion de librerias Python3"
sudo -H pip3 install SpeechRecognition
sudo -H pip3 install unidecode
sudo -H pip3 install paramiko
sudo -H pip3 install cryptography==2.4.2
sudo -H pip3 install mysql-connector-python
sudo -H pip3 install pyaudio
echo "Instalacion de scripts"
echo '#!/usr/bin/python3.5
import time
import sys
import mysql.connector
from datetime import date, datetime
peticion=sys.argv[1]
cnx = mysql.connector.connect(user="LMV_ADMIN", password="LABORATORIOT4", host="10.0.5.246", database='LMV')
cursor = cnx.cursor(buffered=True)
today = datetime.now()
print(today)
print("Codigo Escaneado:"+peticion)
add_proceso = ("INSERT INTO t_modulo4 (codigo_barras, fecha) VALUES ("+peticion+",'"+str(today)+"')")
data_proceso = {"codigo_barras":peticion, "fecha":str(today)}
cursor.execute(add_proceso,)
cnx.commit()' > m.py
chmod +x m.py
echo "Copia del script  bin"
cp m.py /bin/
init 6
