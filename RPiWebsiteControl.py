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
		
	inputList = []
	while ser.in_waiting > 0 :
		line = ser.readline()
		inputList.append(line)
	for thing in inputList:
		print thing
	return 0
	#return replacements

def removePrevHtml():
	if os.path.exists(outfile):
        	os.remove(outfile)
	else:
        	print("The original outfile /var/www/html/index.html does not exist")

def main():
	# initiate main loop:
	
	# get your data from input stream
	replacements = populateData()
	
	# replace it in the template
	#refreshed_template = refresh_data(templateData,replacements)
	
	# remove old 
	#removePrevHtml()	
	
	# write new file to this position
	#with open(outfile,'w+') as outFile:
	#	outFile.write(refreshed_template)

if __name__ == "__main__":
	while 1:
		main()
		time.sleep(120)


