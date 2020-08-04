#!/usr/bin/env python

from __future__ import division
from datetime import datetime
import serial
import re
import os
import time

ser= serial.Serial('/dev/ttyACM0',9600)

outfile = "/var/www/html/index.html"

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
	replacements = {}
	#replacements = {'{light_mode}':'On','{sens1}':75.2,'{sens2}':81.4,'{sens3}':71.2,'{temp_avg}': 79.6,'{temp_stdev}': 0.89,'{pwm_usec}': 32}
	
	#get time and date
	now = datetime.now()
	dateandtime = now.strftime("%d/%m/%Y %H:%M:%S")
	
	replacements.update({'{last_reading}':dateandtime})	

	replacements.update({'{light_mode}':'On'})	
	
	inputList = []
	while ser.in_waiting > 0 :
		line = ser.readline()
		inputList.append(line.strip())
	
	# use regex to strip out data:
	
	regexDict = {'{dutyCycle}':'Duty\ Cycle:([0-9]+.[0-9]+)\ %','{pwmUptime}':'pwmUpTime:([0-9]+.[0-9]+)\ usec','{pwm_freq}':'Initiating\ PWM\ with\ the\ frequency:([0-9]+)','{pwm_usec}':'The\ maximum\ PWM\ uptime\ in\ usec\ is:([0-9]+.[0-9]*)','{reset_cycles}':'Resetting\ after\ every:([0-9]+)\ cycles','{sens1_value}':'Sensor\ 1\ Val:([0-9]+)','{sens1_voltage}':'Sensor\ 1\ Voltage\ Output:([0-9]+.[0-9]+)','{sens1_resistance}':'Sensor\ 1\ Resistance:([0-9]+.[0-9]+)','{sens1}':'Sensor\ 1\ Temperature:([0-9]+.[0-9]+)','{sens2_value}':'Sensor\ 2\ Val:([0-9]+)','{sens2_voltage}':'Sensor\ 2\ Voltage\ Output:([0-9]+.[0-9]+)','{sens2_resistance}':'Sensor\ 2\ Resistance:([0-9]+.[0-9]+)','{sens2}':'Sensor\ 2\ Temperature:([0-9]+.[0-9]+)','{sens3_value}':'Sensor\ 3\ Val:([0-9]+)','{sens3_voltage}':'Sensor\ 3\ Voltage\ Output:([0-9]+.[0-9]+)','{sens3_resistance}':'Sensor\ 3\ Resistance:([0-9]+.[0-9]+)','{sens3}':'Sensor\ 3\ Temperature:([0-9]+.[0-9]+)','{temp_avg}':'Sensor\ Average:([0-9]+.[0-9]+)','{temp_stdev}':'Sensor\ STDEV:([0-9]+.[0-9]+)'}

	# search each line in the 
	for line in inputList:
    		#print line
    		for key,val in regexDict.items():
        		#print val
        		match = re.search(str(val),str(line))
        		if match:
            			#print match.group(1)
            			replacements.update({key:match.group(1)})
	return replacements

def removePrevHtml():
	if os.path.exists(outfile):
        	os.remove(outfile)
	else:
        	print("The original outfile /var/www/html/index.html does not exist")

def main():
	# Initiate main loop:
	
	# get your data from input stream
	replacements = populateData()
	
	# replace it in the template
	refreshed_template = refresh_data(templateData,replacements)
	
	# remove old 
	removePrevHtml()	
	
	# write new file to this position
	with open(outfile,'w+') as outFile:
		outFile.write(refreshed_template)

if __name__ == "__main__":
	while 1:
		if ser.in_waiting > 0 :
			main()
			time.sleep(10)
		else:
			time.sleep(10)

