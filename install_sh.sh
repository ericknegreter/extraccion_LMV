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
sudo apt-get install python3-dev -y
sudo apt-get install python3-mysql.connector -y
sudo apt-get install flac -y
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
sudo -H pip3 install cryptography
sudo -H pip3 install mysql-connector-python
sudo -H pip3 install pyaudio
echo "Instalacion de scripts"
echo '#!/usr/bin/python3.7
import time
import sys
import mysql.connector
from datetime import date, datetime
import Adafruit_DHT

sensor=Adafruit_DHT.DHT11
gpio=7
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
peticion1=sys.argv[1]
cnx1 = mysql.connector.connect( user="LMV_ADMIN", password="MINIMOT4", host="10.0.5.246", database='LMV')
cursor1 = cnx1.cursor()
today1 = datetime.now()
print("Codigo escaneado:"+peticion1)
add_proceso1 = ("INSERT INTO t_modulo2 (codigo_barras, fecha, tmp, hum) VALUES (%(codigo_barras)s, %(fecha)s, %(tmp)s, %(hum)s)")
data_proceso1 = {'codigo_barras':peticion1, 'fecha':today1, 'tmp':temperature, 'hum':humidity}
cursor1.execute(add_proceso1, data_proceso1)
cnx1.commit()
cursor1.close()
print("Conexion cerrada")' > m.py
chmod +x m.py
echo "Copia del script  bin"
cp m.py /bin/
init 6
