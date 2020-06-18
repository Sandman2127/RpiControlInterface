#!/usr/bin/env python

from __future__ import division
from datetime import datetime
import serial
import re

#ser= serial.Serial('/dev/ttyUSBx',9600)

#readin template data

template = '/home/pi/Desktop/Programs_and_Scripts/RPiWebsiteControl/lib/html/controlInterface.html'
with open(template,'r') as f:
	templateData = f.read()
	f.close()

def refresh_data(templateData,inputDict):
	for key,val in inputDict.items():
		templateData = templateData.replace(key,str(val))
	return templateData

def populateData():
	#replacements = {}
	replacements = {'{light_mode}':'on','{temp_avg}': 1 ,'{temp_stdev}': 2,'{pwm_usec}': 3}
	

	#get time and date
	now = datetime.now()
	dateandtime = now.strftime("%d/%m/%Y %H:%M:%S")
	replacements.update({'{last_reading}':dateandtime})	
	
	#parse input string to get other values
	

	return replacements

def main():
	replacements = populateData()
	refreshed_template = refresh_data(templateData,replacements)
	print(refreshed_template)
	#while 1:
        	#print "stuff"
        	#if(ser.in_waiting > 0):
        	#       line = ser.readline()
        	#       print(line)	

if __name__ == "__main__":
	main()


