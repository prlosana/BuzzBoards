#-------------------------------------------------------------------------------
# Name:         wear_multiplexer_reader.py
# Purpose:      Used to read two PCA9547 multiplexers (16 channels) for FortiTo's BuzzWear Sensors
# Author:       Anasol Pena-Rios
# Created:      15/04/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class WearMultiplexerReader():

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used
	address_multiplexerA	= 0x71              #address
	address_multiplexerB	= 0x70              #address

	#Registers
	#-------------------------------------------------------------------------------	
	__reset_channel			= 0x0
	__channel0				= 0x8
	__channel1				= 0x9
	__channel2				= 0xA
	__channel3				= 0xB
	__channel4				= 0xC
	__channel5				= 0xD
	__channel6				= 0xE
	__channel7				= 0xF
		
	def __init__(self, busToUse = 0, debug = False):	
		pass
	
	def getChannel(self, busToUse = 0, debug = False):
		current = 0
		
		#Read values assigned
		bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1

		multiplexerA = bus.read_byte(self.address_multiplexerA)	
		if (debug):
			print "DEBUG - multiplexer1 ---- Binary value = ", bin(multiplexerA), ", Value read = ", multiplexerA

		multiplexerB = bus.read_byte(self.address_multiplexerB)	
		if (debug):
			print "DEBUG - multiplexer2 ---- Binary value = ", bin(multiplexerB), ", Value read = ", multiplexerB
					
		if (multiplexerA <> self.__reset_channel):
			#Between channels 1-8
			if (multiplexerA == self.__channel0):
				current = 9
			elif (multiplexerA == self.__channel1):	
				current = 10
			elif (multiplexerA == self.__channel2):	
				current = 11
			elif (multiplexerA == self.__channel3):	
				current = 12
			elif (multiplexerA == self.__channel4):	
				current = 13
			elif (multiplexerA == self.__channel5):	
				current = 14
			elif (multiplexerA == self.__channel6):	
				current = 15
			elif (multiplexerA == self.__channel7):	
				current = 16
		else:
			#Between channels 9-16
			if (multiplexerB == self.__channel0):
				current = 1
			elif (multiplexerB == self.__channel1):	
				current = 2
			elif (multiplexerB == self.__channel2):	
				current = 3
			elif (multiplexerB == self.__channel3):	
				current = 4
			elif (multiplexerB == self.__channel4):	
				current = 5
			elif (multiplexerB == self.__channel5):	
				current = 6
			elif (multiplexerB == self.__channel6):	
				current = 7
			elif (multiplexerB == self.__channel7):	
				current = 8
		
		if (debug):		
			print "MULTIPLEXER READER - Get current channel "	, current
		
		return current

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running MULTIPLEXER READER test")
	print ("----------------------------------------------------")

	#Select multiplexer / Channel
	#-------------------------------------------------------------------------------	
	try:
		channel = 0
		multiplexerReader = WearMultiplexerReader()
		channel = multiplexerReader.getChannel(1)
		print "MULTIPLEXER READER - Current channel selected ",channel

	except Exception as e: 
		print "ERROR: MULTIPLEXER READER - ", e
		
	print ("----------------------------------------------------")
	print ("finished - MULTIPLEXER READER  test")
	print ("----------------------------------------------------")		