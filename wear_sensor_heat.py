#-------------------------------------------------------------------------------
# Name:         wear_sensor_heat.py
# Purpose:      Use tmp175 to measure temperature for FortiTo's BuzzWear Sensors. Temperature range -40 to 125c	
# Author:       Anasol Pena-Rios
# Created:      15/04/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class WearSensorHeat():

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used
	address_heatsensor		= 0x4E              #address

	#Registers
	#-------------------------------------------------------------------------------
	__temp_reg_temperature	= 0x0
	__temp_reg_config		= 0x1
	__temp_reg_datalow		= 0x2
	__temp_reg_datahigh		= 0x3

	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0
	read_val = 0
	decimals = False

	def __init__(self, busToUse = 0):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1
		self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x00) #reset

	def clean(self, debug = False):
		# Initialise values
		self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x00) #reset
		
		if (debug):
			ctrl = self.bus.read_byte_data(self.address_heatsensor,self.__temp_reg_config)
			print "HEAT SENSOR - initialisation --- Binary values = ", bin(ctrl), ", Value read = ", ctrl
			
	def setPrecision(self, noDecimals):
		# Set Precision value	
		if noDecimals == 0:
			self.decimals = False
			self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x00) #1			
		elif noDecimals == 1:
			self.decimals = True
			self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x00) #1
		elif noDecimals == 2:
			self.decimals = True
			self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x20) #2
		elif noDecimals == 3:
			self.decimals = True
			self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x40) #3
		elif noDecimals == 4:
			self.decimals = True
			self.bus.write_byte_data(self.address_heatsensor,self.__temp_reg_config, 0x60) #4
		else:
			return "ERROR - Precision value invalid."
		
		return "OK"
		
	def getTemperature(self, debug = False):
		# Get value from HEAT sensor
		temperature = 0 
		temp_float = 0

		"""	
		# Obtain integer temperature value in Celsius
		read_val = bus.read_byte(address_heatsensor)	
		time.sleep(0.2) #0.2 second
		print "HEAT SENSOR ---- Binary values = ", bin(read_val), ", Value read = ", read_val
		"""
		read_val = self.bus.read_i2c_block_data(self.address_heatsensor, self.__temp_reg_temperature)
		hi0 = read_val[0]
		lo0 = read_val[1]

		if (debug):		
			print "HEAT SENSOR - values ---- Binary values hi0 ", bin(hi0), ", lo0 ", bin(lo0)
			#ctrl = self.bus.read_byte_data(self.address_heatsensor,__self.temp_reg_config)
			#print "HEAT SENSOR - CONTROL REGISTRY --- Binary values = ", bin(ctrl), ", Value read = ", ctrl

		if self.decimals == True:
			if lo0 != 0:
				temp_float = (lo0 * 0.9375)/240

			if hi0 >= 128:
				# temp_sign = negative
				if hi0 == 255:
					temperature = 0 - temp_float
				else:
					temperature = (temperature - 256) - temp_float
			else:
				temperature = hi0 + temp_float
		else:
			if hi0 >= 128:
				# temp_sign = negative
				if hi0 == 255:
					temperature = 0
				else:
					temperature = (temperature - 256)
			else:
				temperature = hi0
				
		return temperature	


if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running TEMPERATURE SENSOR test")
	print ("----------------------------------------------------")

	#Heat sensor
	#------------------------------------------------------------------------------
	try:
		result = ""
		temperatureSensor = WearSensorHeat(1)
		decimals = 4
		read_val = temperatureSensor.setPrecision(decimals)
		print "HEAT SENSOR - Set precision, no. of decimals =", decimals, ". Result - ", read_val
		
		if read_val == "OK":
			while True:
				result = temperatureSensor.getTemperature()		
				print "HEAT SENSOR - Temperature ", result, " C"

	except Exception as e: 
		print "ERROR: HEAT SENSOR - ", e

	print ("----------------------------------------------------")
	print ("finished - TEMPERATURE SENSOR test")
	print ("----------------------------------------------------")
