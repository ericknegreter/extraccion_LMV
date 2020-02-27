import Adafruit_DHT
import mysql.connector
import time
import subprocess, datetime

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio=7

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
    if ping(localhost):
        print ("[%s] Network is up!" % str(datetime.datetime.now()))
        xstatus = 0
    
    if xstatus:
        time.sleep(10)
        print ("[%s] Network is down :(" % str(datetime.datetime.now()))
        time.sleep(25)

    return xstatus

while True:
    try:
        # Use read_retry method. This will retry up to 15 times to
        # get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        # Reading the DHT11 is very sensitive to timings and occasionally
        # the Pi might fail to get a valid reading. So check if readings are valid.
        if humidity is not None and temperature is not None:
            #Time taken to restart networking
            time.sleep(20)
            #End the time sleep
            while True:
                if(net_is_up() == 0):
                    #Connection to database LMV and insert on temperature and humidity table new field with mysql
                    #temperature
                    mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="MINIMOT4", database="LMV")
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO temperature (tmp, area) VALUES (%s, %s)"
                    val = (temperature, 'extraccion')
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
                    #humidity
                    sql = "INSERT INTO humidity (hum, area) VALUES (%s, %s)"
                    val = (humidity, 'extraccion')
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
                    #END of mysql
                    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
                    break
            break    
        else:
            print('Failed to get reading. Try again!')
    except ValueError:
        print("Measurement stopped by Error")
    except OSError as err:
        print("OS error: {0}".format(err))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
