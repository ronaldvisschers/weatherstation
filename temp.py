import os
import glob
import time
import datetime
import sys
import MySQLdb
import my_sqlm
from datetime import datetime
import requests
import logging


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c

logger.info('start reading temperature BS18')
temperatureInside = read_temp()
print temperatureInside

# write the data to the mysql database
currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

sqlCommand = "INSERT INTO thpdata (dateandtime, temp_in) VALUES ('%s','%s')"% (currentTime, temperatureInside)
print sqlCommand
try:
    my_sqlm.databaseHelper(sqlCommand,"Insert")
except:
	print "can not write to database"
	sys.exit(0)

