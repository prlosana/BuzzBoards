#-------------------------------------------------------------------------------
# Name:         wear_multiplexer.py
# Purpose:      Use two PCA9547 to control multiplexer (16 channels) for FortiTo's BuzzWear Sensors
# Author:       Anasol Pena-Rios
# Created:      15/04/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class WearMultiplexer():

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

	#Attributes
	#-------------------------------------------------------------------------------
	current_channel = 0
		
	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0		
	read_val = 0
	
	def __init__(self, busToUse = 0, debug = False):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1	
		#Initialise multiplexers
		self.bus.write_byte(self.address_multiplexerA, self.__reset_channel) #set value	
		time.sleep(0.2) #0.2 second

		self.bus.write_byte(self.address_multiplexerB, self.__reset_channel) #set value	
		time.sleep(0.2) #0.2 second
		
		#Set channel 1 as default channel
		self.bus.write_byte(self.address_multiplexerA, self.__channel0)
		self.current_channel = 1
		
		if (debug):
			print "MULTIPLEXERS - Initialising board "

	def clean(self, debug = False):
		#Initialise multiplexers
		self.bus.write_byte(self.address_multiplexerA, self.__reset_channel) #set value	
		time.sleep(0.2) #0.2 second

		self.bus.write_byte(self.address_multiplexerB, self.__reset_channel) #set value	
		time.sleep(0.2) #0.2 second
		
		if (debug):
			print "MULTIPLEXERS - Cleaning channels "
	
	def getChannel(self, debug = False):
		current = 0
		#Read values assigned
		multiplexerA = self.bus.read_byte(self.address_multiplexerA)
		multiplexerB = self.bus.read_byte(self.address_multiplexerB)
		
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
				
		self.current_channel = current
		
		if (debug):
			print "MULTIPLEXERS - Get current channel "	, self.current_channel
		return self.current_channel
	
	def setChannel(self, channel, debug = False):	
		#The multiplexer board has one I2C input and 16 outputs going to the sensors. 
		#The multiplexer utilizes 2 PCA9547's. First PCA9547 has channels 0-7. Second has channels 8-15 
		#When one is selected and active the other must be deactivated.
		self.clean(debug)
		
		#Select channel
		if channel == 1:
			self.bus.write_byte(self.address_multiplexerB, self.__channel0)
		elif channel == 2:
			self.bus.write_byte(self.address_multiplexerB, self.__channel1)	
		elif channel == 3:
			self.bus.write_byte(self.address_multiplexerB, self.__channel2)	
		elif channel == 4:
			self.bus.write_byte(self.address_multiplexerB, self.__channel3)	
		elif channel == 5:
			self.bus.write_byte(self.address_multiplexerB, self.__channel4)	
		elif channel == 6:
			self.bus.write_byte(self.address_multiplexerB, self.__channel5)	
		elif channel == 7:
			self.bus.write_byte(self.address_multiplexerB, self.__channel6)	
		elif channel == 8:
			self.bus.write_byte(self.address_multiplexerB, self.__channel7)	
		elif channel == 9:
			self.bus.write_byte(self.address_multiplexerA, self.__channel0)	
		elif channel == 10:
			self.bus.write_byte(self.address_multiplexerA, self.__channel1)	
		elif channel == 11:
			self.bus.write_byte(self.address_multiplexerA, self.__channel2)	
		elif channel == 12:
			self.bus.write_byte(self.address_multiplexerA, self.__channel3)	
		elif channel == 13:
			self.bus.write_byte(self.address_multiplexerA, self.__channel4)	
		elif channel == 14:
			self.bus.write_byte(self.address_multiplexerA, self.__channel5)	
		elif channel == 15:
			self.bus.write_byte(self.address_multiplexerA, self.__channel6)	
		elif channel == 16:
			self.bus.write_byte(self.address_multiplexerA, self.__channel7)	
		else:
			return "ERROR"

		self.current_channel = channel	
		time.sleep(0.2) #0.2 second	

		if (debug):
			# Get value from multiplexers
			read_val = self.bus.read_byte(self.address_multiplexerA)	
			time.sleep(0.2) #0.2 second
			print "DEBUG - multiplexer1 ---- Binary value = ", bin(read_val), ", Value read = ", read_val

			read_val = self.bus.read_byte(self.address_multiplexerB)	
			time.sleep(0.2) #0.2 second
			print "DEBUG - multiplexer2 ---- Binary value = ", bin(read_val), ", Value read = ", read_val

		return "OK"


if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running MULTIPLEXER test")
	print ("----------------------------------------------------")

	#Select multiplexer / Channel
	#-------------------------------------------------------------------------------	
	try:
		result = ""
		multiplexer = WearMultiplexer(1)

		channel = 9
		result = multiplexer.setChannel(channel)
		print "MULTIPLEXER - Enabling channel ",channel," in the board... ", result
		
		channel = multiplexer.getChannel()
		print "MULTIPLEXER - Current channel selected ",channel

	except Exception as e: 
		print "ERROR: MULTIPLEXER - ", e
		
	print ("----------------------------------------------------")
	print ("finished - MULTIPLEXER test")
	print ("----------------------------------------------------")
