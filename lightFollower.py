#-------------------------------------------------------------------------------
# Name:         lightFollower.py
# Purpose:      Use light follower sensors for FortiTo's BuzzBot
# Author:       Anasol Pena-Rios
# Created:      20/02/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class lightFollower():

    #I2C Addresses
    #-------------------------------------------------------------------------------
	bus         	= smbus.SMBus(0)    #open the bus on /dev/i2c-0
	address_sensors	= 0x31              #address
    
    #Global variables
    #-------------------------------------------------------------------------------
	read_val = 255
    
	def __init__(self):
		# Initialise values
		self.read_val = 0
	
	def clean(self):
		# Clean values
		self.read_val = 0

	def setSensitivity(self, value, debug = False):
		# Write values - Default value 0
		# 0 - low , 1 - medium, 2 - high, 3 - very high (Do not use)
		msg = ""
		
		if value in (0,1,2):
			self.bus.write_byte(self.address_sensors, value) #set value	
			time.sleep(0.2) #0.2 second
			msg = "OK"
		else:
			msg = "ERROR: Wrong value"
			
		if debug:
			print "Set sensitivity: ", msg
		
		return msg

	def getDirection(self, debug = False):
		result = ""

		# Read values - Default value 0
		self.read_val = self.bus.read_byte(self.address_sensors)	
		time.sleep(0.2) #0.2 second

		if self.read_val == 0:
			result = "NO LIGHT"
		elif self.read_val == 1:
			result = "RIGHT"
		elif self.read_val == 2:
			result = "LEFT"
		elif self.read_val == 3:
			result = "BOTH"
		else:
			result = "ERROR"  
		
		if debug:
			print "Binary values = ", bin(self.read_val)
			print self.read_val, " Value read."
			print "Direction ", result 
				
		return result 

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running LIGHT FOLLOWER test")
	print ("----------------------------------------------------")
	
	result = ""
	lightSensor = lightFollower()
	lightSensor.clean()
	result = lightSensor.setSensitivity(1, True)
	
	while 1:
		result = lightSensor.getDirection (True)

	print ("----------------------------------------------------")
	print ("finished - LIGHT FOLLOWER test")
	print ("----------------------------------------------------")