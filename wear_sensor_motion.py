#-------------------------------------------------------------------------------
# Name:         wear_sensor_motion.py
# Purpose:      Use MMA7660FC accelerometer
# Author:       Anasol Pena-Rios
# Created:      30/04/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class WearSensorMotion():

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used
	
	address_motionsensor		= 0x4C              #address

	#Registers
	#-------------------------------------------------------------------------------
	__temp_reg_XOUT		= 0x0
	__temp_reg_YOUT		= 0x1
	__temp_reg_ZOUT		= 0x2
	__temp_reg_TILT		= 0x3
	__temp_reg_SRST		= 0x4
	__temp_reg_SPCNT	= 0x5
	__temp_reg_INTSU	= 0x6
	__temp_reg_MODE		= 0x7
	__temp_reg_SR		= 0x8
	__temp_reg_PDET		= 0x9
	__temp_reg_PD		= 0xA

	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0
	read_val = 0
	decimals = False

	def __init__(self, busToUse = 0):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1

		# Set 1 Sample/Second and Auto-Sleep Mode
		self.bus.write_byte_data(self.address_motionsensor,self.__temp_reg_SR, 0x1F)

		# Set AutoWake ON and Active mode
		self.bus.write_byte_data(self.address_motionsensor,self.__temp_reg_MODE, 0x0B)		

	def clean(self, debug = False):
		# Set 1 Sample/Second and Auto-Sleep Mode
		self.bus.write_byte_data(self.address_motionsensor,self.__temp_reg_SR, 0x1F)

		# Set AutoWake ON and Active mode
		self.bus.write_byte_data(self.address_motionsensor,self.__temp_reg_MODE, 0x0B)		
		
	def getPosition(self, debug = False):
		alert = 1
		tilt = "UNKNOWN"
		
		while (alert):
			valRead = self.bus.read_byte_data(self.address_motionsensor, self.__temp_reg_TILT)
			alert = int(valRead>>6)
			#if (debug):
				#print "MOTION SENSOR - Alert TILT = ", alert		
		
		bitLength = valRead.bit_length()
		if (debug):
			print "MOTION SENSOR - TILT - bitLenght = ", bitLength
		
		#BACK - FRONT
		if (bitLength > 2):
			subvalBaFro = bin(valRead)[-2:]
		else:
			subvalBaFro = bin(valRead)
			
		subvalBaFroInt = int(subvalBaFro, 2)
		
		if (subvalBaFroInt == 1):
			tilt = "FRONT"
		elif (subvalBaFroInt == 2):
			tilt = "BACK"
		else:
			tilt = "UNKNOWN"
			
		if (debug):
			print "MOTION SENSOR - TILT = ", bin(valRead), ", Value read = ", valRead
			print "MOTION SENSOR - TILT - Back-Front = ", subvalBaFro, ", Value read = ", subvalBaFroInt

		return tilt

	def getOrientation(self, debug = False):
		alert = 1
		tilt = "UNKNOWN"
		
		while (alert):
			valRead = self.bus.read_byte_data(self.address_motionsensor, self.__temp_reg_TILT)
			alert = int(valRead>>6)
			#if (debug):
				#print "MOTION SENSOR - Alert TILT = ", alert		
		
		bitLength = valRead.bit_length()
		if (debug):
			print "MOTION SENSOR - TILT - bitLenght = ", bitLength

		#LEFT - RIGHT - DOWN - UP
		if (bitLength >= 5):
			subvalPoLa = bin(valRead)[-5:-2]
			subvalPoLaInt = int(subvalPoLa, 2)
		else:
			subvalPoLa = bin(valRead)
			subvalPoLaInt = 0

		if (subvalPoLaInt == 1):
			tilt = "LEFT"
		elif (subvalPoLaInt == 2):
			tilt = "RIGHT"
		elif (subvalPoLaInt == 5):
			tilt = "DOWN"
		elif (subvalPoLaInt == 6):
			tilt = "UP"			
		else:
			tilt = "UNKNOWN"
			
		if (debug):
			print "MOTION SENSOR - TILT = ", bin(valRead), ", Value read = ", valRead
			print "MOTION SENSOR - TILT - Left-Right-Down-Up = ", subvalPoLa, ", Value read = ", subvalPoLaInt

		return tilt
		
	def getXAxis(self, debug = False):
		# Get value from ACCELEROMETER (Range from +31 to -32)
		subvalueX = 0
		result = 0
		alert = 1
		
		while (alert):
			valueX = self.bus.read_byte_data(self.address_motionsensor, self.__temp_reg_XOUT)
			alert = int(valueX>>6)
			if (debug):
				print "MOTION SENSOR - Alert X = ", alert
		
		bitLength = valueX.bit_length()
		if (debug):
			print "MOTION SENSOR - X - bitLenght = ", bitLength
			
		if (bitLength > 5):
			subvalueX = bin(valueX)[-5:] 
		else:
			subvalueX = bin(valueX)
			
		sign = int(valueX>>5)
		
		if (sign == 1):
			result = int(subvalueX, 2) * -1
		else:
			result = int(subvalueX, 2)
			
		if (debug):
			print "MOTION SENSOR - X Axis = ", bin(valueX), ", Value read = ", valueX	
			print "MOTION SENSOR - Value = ", subvalueX, ", Value read = ", int(subvalueX, 2)
			print "MOTION SENSOR - Sign = ", sign	
			print "MOTION SENSOR - Result = ", result	
		
		return result	

	def getYAxis(self, debug = False):
		# Get value from ACCELEROMETER (Range from +31 to -32)
		subvalueY = 0
		result = 0
		alert = 1
		
		while (alert):		
			valueY = self.bus.read_byte_data(self.address_motionsensor, self.__temp_reg_YOUT)
			alert = int(valueY>>6)
			if (debug):
				print "MOTION SENSOR - Alert Y = ", alert
				
		bitLength = valueY.bit_length()
		if (debug):
			print "MOTION SENSOR - Y - bitLenght = ", bitLength
			
		if (bitLength > 5):
			subvalueY = bin(valueY)[-5:] 
		else:
			subvalueY = bin(valueY)
			
		sign = int(valueY>>5)
		
		if (sign == 1):
			result = int(subvalueY, 2) * -1
		else:
			result = int(subvalueY, 2)
			
		if (debug):
			print "MOTION SENSOR - Y Axis = ", bin(valueY), ", Value read = ", valueY	
			print "MOTION SENSOR - Value = ", subvalueY, ", Value read = ", int(subvalueY, 2)
			print "MOTION SENSOR - Sign = ", sign	
			print "MOTION SENSOR - Result = ", result	
		
		return result	

	def getZAxis(self, debug = False):
		# Get value from ACCELEROMETER (Range from +31 to -32)
		subvalueZ = 0
		result = 0
		alert = 1
		
		while (alert):			
			valueZ = self.bus.read_byte_data(self.address_motionsensor, self.__temp_reg_ZOUT)
			alert = int(valueZ>>6)
			if (debug):
				print "MOTION SENSOR - Alert Z = ", alert
				
		bitLength = valueZ.bit_length()
		if (debug):
			print "MOTION SENSOR - Z - bitLenght = ", bitLength
			
		if (bitLength > 5):
			subvalueZ = bin(valueZ)[-5:] 
		else:
			subvalueZ = bin(valueZ)
			
		sign = int(valueZ>>5)
		
		if (sign == 1):
			result = int(subvalueZ, 2) * -1
		else:
			result = int(subvalueZ, 2)
			
		if (debug):
			print "MOTION SENSOR - Z Axis = ", bin(valueZ), ", Value read = ", valueZ	
			print "MOTION SENSOR - Value = ", subvalueZ, ", Value read = ", int(subvalueZ, 2)
			print "MOTION SENSOR - Sign = ", sign		
			print "MOTION SENSOR - Result = ", result	
		
		return result	

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running MOTION SENSOR test")
	print ("----------------------------------------------------")

	try:
		result = ""
		motionSensor = WearSensorMotion(1)
		print "MOTION SENSOR - started ="
		
		while True:
			x = motionSensor.getXAxis()		
			y = motionSensor.getYAxis()		
			z = motionSensor.getZAxis()		
			print "MOTION SENSOR - X=", x, ", Y=", y, ", Z=", z
			tilt = motionSensor.getPosition()
			print "MOTION SENSOR - POSITION=", tilt
			tilt = motionSensor.getOrientation()
			print "MOTION SENSOR - ORIENTATION=", tilt
		
	except Exception as e: 
		print "ERROR: MOTION SENSOR - ", e

	print ("----------------------------------------------------")
	print ("finished - MOTION SENSOR test")
	print ("----------------------------------------------------")
