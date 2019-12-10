import time
import sys
import mysql.connector
from datetime import date, datetime
import Adafruit_DHT

sensor=Adafruit_DHT.DHT11
gpio=17
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
peticion1=sys.argv[1]
cnx1 = mysql.connector.connect( user="LMV_ADMIN", password="LABORATORIOT4", host="10.0.5.246", database='LMV')
cursor1 = cnx1.cursor()
today1 = datetime.now()
print("Codigo escaneado:"+peticion1)
add_proceso1 = ("INSERT INTO t_modulo2 (codigo_barras, fecha, tmp, hum) VALUES (%(codigo_barras)s, %(fecha)s, %(tmp)s, %(hum)s)")
data_proceso1 = {'codigo_barras':peticion1, 'fecha':today1, 'tmp':temperature, 'hum':humidity}
cursor1.execute(add_proceso1, data_proceso1)
cnx1.commit()
cursor1.close()
print("Conexion cerrada")