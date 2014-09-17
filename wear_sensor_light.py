#-------------------------------------------------------------------------------
# Name:         wear_sensor_light.py
# Purpose:      Use APDS-9300 to measure light intensity for FortiTo's BuzzWear Sensors
# Author:       Anasol Pena-Rios
# Created:      15/04/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class WearSensorLight():

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used
	address_lightsensor		= 0x49              #address

	#Registers
	#-------------------------------------------------------------------------------
	__light_reg_control		= 0xE0
	__light_reg_timing		= 0xE1
	__light_reg_threshlowlo	= 0xE2
	__light_reg_threshlowhi	= 0xE3
	__light_reg_threshhighlo	= 0xE4
	__light_reg_threshhighhi	= 0xE5
	__light_reg_interrupt		= 0xE6
	__light_reg_data0low		= 0xEC
	__light_reg_data0high		= 0xED
	__light_reg_data1low		= 0xEE
	__light_reg_data1high		= 0xEF

	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0	
	read_val = 0

	def __init__(self, busToUse = 0, debug = False):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1	
		ctrl = self.bus.read_byte_data(self.address_lightsensor,self.__light_reg_control)
		
		if (debug):
			print "LIGHT SENSOR ---- Binary values = ", bin(ctrl), ", Value read = ", ctrl

		while ctrl <> 3: #Read contents of Control register to verify communication
			#Initialise light sensor
			self.bus.write_byte_data(self.address_lightsensor,self.__light_reg_control, 0x00) #power down
			self.bus.write_byte_data(self.address_lightsensor,self.__light_reg_control, 0x03) #power up
			time.sleep(0.2) #0.2 second
			ctrl = self.bus.read_byte_data(self.address_lightsensor,self.__light_reg_control)
			
		if (debug):
			print "LIGHT SENSOR - powered up successfully ---- Binary values = ", bin(ctrl), ", Value read = ", ctrl

		# Get value from LIGHT sensor
		read_val = self.bus.read_byte(self.address_lightsensor)	
		time.sleep(0.2) #0.2 second
		if (debug):
			print "LIGHT SENSOR - read ---- Binary values = ", bin(read_val), ", Value read = ", read_val

	def clean(self, debug = False):
		#Initialise light sensor
		self.bus.write_byte_data(self.address_lightsensor,self.__light_reg_control, 0x00) #power down
		self.bus.write_byte_data(self.address_lightsensor,self.__light_reg_control, 0x03) #power up
		time.sleep(0.2) #0.2 second
		ctrl = self.bus.read_byte_data(self.address_lightsensor,self.__light_reg_control)
			
		if (debug):
			print "LIGHT SENSOR - Clean ---- Binary values = ", bin(ctrl), ", Value read = ", ctrl

	def getLux(self, debug = False):
		"""
		# This reads all values (hi & low) from both channels (0-1)
		reading = self.bus.read_i2c_block_data(address_lightsensor, light_reg_data0low)
		lo0 = reading[0]
		hi0 = reading[1]
		lo1 = reading[2]
		hi1 = reading[3]
		if (debug):
			print "LIGHT SENSOR - values ---- Binary values lo0 ", bin(lo0), ", lo1 ", bin(lo1), ", hi0 ", bin(hi0), ", hi1 ", bin(hi1)
			print "LIGHT SENSOR - values ---- values lo0 ", lo0, ", lo1 ", lo1, ", hi0 ", hi0, ", hi1 ", hi1
		"""
		reading = self.bus.read_word_data(self.address_lightsensor, self.__light_reg_data0low)
		if (debug):
			print "LIGHT SENSOR - values WORD ---- Binary values = ", bin(reading), ", Value read = ", reading	
		return reading


if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running LIGHT SENSOR test")
	print ("----------------------------------------------------")

	#Light sensor
	#-------------------------------------------------------------------------------
	try:	
		result = ""
		lightSensor = WearSensorLight(1)
		
		while True:
			result = lightSensor.getLux()
			print "LIGHT SENSOR - Lux ", result	
			
	except Exception as e: 
		print "ERROR: LIGHT SENSOR - ", e

	print ("----------------------------------------------------")
	print ("finished - LIGHT SENSOR test")
	print ("----------------------------------------------------")
