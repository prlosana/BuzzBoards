#-------------------------------------------------------------------------------
# Name:         lineFollower.py
# Purpose:      Use line follower sensors for FortiTo's BuzzBot
# Author:       Anasol Pena-Rios
# Created:      19/02/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class lineFollower():

    #I2C Addresses
    #-------------------------------------------------------------------------------
	bus         	= smbus.SMBus(0)    #open the bus on /dev/i2c-0
	address_sensors	= 0x30              #address
    
    #Global variables
    #-------------------------------------------------------------------------------
	read_val = 255

	def __init__(self):
		# Initialise values
		self.read_val = 255

	def clean(self):
		# Clean values
		self.read_val = 255

	def setLineBias(self, value, debug = False):
		# Write values - Default value 0
		# 0 = Black or white line no bias.
		# 1 = Black line bias
		# 2 = White line bias
		# 3 = Automatic black or white bias
		msg = ""
		
		if value in (0,1,2,3):
			self.bus.write_byte(self.address_sensors, value) #set value	
			time.sleep(0.2) #0.2 second
			msg = "OK"
		else:
			msg = "ERROR: Wrong value"
			
		if debug:
			print "Set Line Bias: ", msg
		
		return msg
				
	def getDirection(self, debug = False):
		result = ""

		# Read values - Default value 255 (0xFF)
		self.read_val = self.bus.read_byte(self.address_sensors)	
		time.sleep(0.2) #0.2 second

		if self.read_val == 0:
			result = "NO LINE"
		elif self.read_val in (1,2,3,5,6,7,13,15,19,22,23):
			result = "RIGHT"
		elif self.read_val in (4,10,11,14,27):
			result = "CENTRE"
		elif self.read_val in (8,12,13,15,16,20,24,25,26,28,29,30):
			result = "LEFT"
		else:
			result = "ERROR"  
		
		if debug:
			print "Binary values = ", bin(self.read_val)
			print self.read_val, " Value read."
			print "Direction ", result  	 
				
		#return result
                return self.read_val

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running LINE FOLLOWER test")
	print ("----------------------------------------------------")
	
	result = ""
	lineSensor = lineFollower()
	lineSensor.clean()
	lineSensor.setLineBias(1, True)

	while 1:
		result = lineSensor.getDirection (True)

	print ("----------------------------------------------------")
	print ("finished - LINE FOLLOWER test")
	print ("----------------------------------------------------")
