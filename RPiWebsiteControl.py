#!/usr/bin/env python

from __future__ import division
import serial

#ser= serial.Serial('/dev/ttyUSBx',9600)

#open and work on data
template = '/home/pi/Desktop/Programs_and_Scripts/RPiWebsiteControl/testdoc.txt'
with open(template,'r') as f:
	templateData = f.read()
	f.close()

def refresh_data(templateData,inputDict):
	for key,val in inputDict.items():
		templateData = templateData.replace(key,str(val))
	return templateData
	

def main():
	replacements = { '<random_data>': 1 ,'<random_data2>': 2,'<random_data3>': 3}
	refreshed_template = refresh_data(templateData,replacements)
	print(refreshed_template)
	#while 1:
        	#print "stuff"
        	#if(ser.in_waiting > 0):
        	#       line = ser.readline()
        	#       print(line)	

if __name__ == "__main__":
	main()


