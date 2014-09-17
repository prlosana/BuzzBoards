#-------------------------------------------------------------------------------
# Name:         buzzbox.py
# Purpose:      Use PCA9533 to control FortiTo's BuzzBox
#               PCA9533 - 2 selectable, fully programmable blink rates
#               (frequency and duty cycle)
# Author:       Anasol Pena-Rios
# Created:      28/01/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

#-----------------------------------------------------------------------
# NOTE1: To PWM allows to set a blinking light
#-----------------------------------------------------------------------
# The following example will show how to set LED0 to blink at 1 Hz at a 50 % duty cycle
# Set pre scaler PSC to achieve a period of 1 second:
#   Blink period = (PSC + 1)/152  Where 152 is the frequency (Hz) of the device        
#   __PSC = Blink period = 1seg = (PSC + 1)/152
#   Then (1*152)-1 = PSC

# Set PWM duty cycle to 50 %:
#   PWM / 256 = 0.5
#   __PWM = 0.5 * 256
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# NOTE2: To PWM allows to set a dimming light
#-----------------------------------------------------------------------
# The LED brightness is controlled by setting the
# blink rate high enough (> 100 Hz) that the blinking cannot be seen and then using the duty
# cycle to vary the amount of time the LED is on and thus the average current through the LED
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# NOTE 3: KAU Project
#-----------------------------------------------------------------------
# FOR KAU Boxes values are inverted for lights 1 & 2 , fan and heater (e.g ON = 00 instead of original OFF = 00)

import smbus
import time
import math

class BuzzBox():
	#PIN DESCRIPTION
	#-------------------------------------------------------------------------------
	#Pin 1 = LED0   - LED driver 0
	#Pin 2 = LED1   - LED driver 1
	#Pin 3 = LED2   - LED driver 2
	#Pin 4 = Vss    - supply ground
	#Pin 5 = LED3   - LED driver 3
	#Pin 6 = SCL    - serial clock line (I2C)
	#Pin 7 = SDA    - serial data line  (I2C)
	#Pin 8 = Vdd    - supply voltage

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used
	address     = 0x63              #PCA9550 address

	#Defining all sub addresses from Control Register Definition DataSheet
	#-------------------------------------------------------------------------------
	__INPUT  = 0x00      #Input register
	__PSC0   = 0x01      #pre-scaler 0
	__PWM0   = 0x02      #Pulse Width Modulator 0
	__PSC1   = 0x03      #pre-scaler 1
	__PWM1   = 0x04      #Pulse Width Modulator 1
	__LS0    = 0x05      #led selector

	#Attributes
	#-------------------------------------------------------------------------------
	status_fan = "OFF"
	status_light1 = "OFF"
	status_light2 = "OFF"
	status_heater = "OFF"

	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0
	internal_val = 0
	val = "00000000"
	light1 = "00"
	light2 = "00"
	fan = "00"
	heater = "00"

	def __init__(self, busToUse = 0):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1

		#Internal value
		#-----------------------------------------------------------------------
		self.val = self.light2 + self.light1 + self.fan + self.heater
		self.internal_val = int(self.val, 2)

		self.setBlink1(1, 0.5, 152)		#blink_period=1, duty_cycle=0.5 (dim value (1-0)), frequency(Hz)=152 (taken from documentation)
		self.setBlink2(1, 0.05, 1)		

		#Verify that all the devices are off
		#-----------------------------------------------------------------------
		#self.setLighting1 (False, 0, False)
		#self.setLighting2 (False, 0, False)
		#self.setFan (False)
		#self.setHeater (False)	
	
	def clean(self):
		self.internal_val = int("00000000", 2)

		#Verify that all the devices are off
		#-----------------------------------------------------------------------
		self.setLighting1 (False, 0, False)
		self.setLighting2 (False, 0, False)
		self.setFan (False)
		self.setHeater (False)			

	def setBlink1(self, blink_period=1, duty_cycle=0.5, frecuency=152):
		#-----------------------------------------------------------------------
		#Set pre-scaler PSC0 to achieve a certain blink period
		#-----------------------------------------------------------------------
		self.PSC0_value = blink_period * frecuency - 1
		self.PSC0_value = int(math.floor(self.PSC0_value))
		self.bus.write_byte_data(self.address, self.__PSC0, self.PSC0_value) #set value
		time.sleep(0.005) #at least 500 microseconds required for set

		#-----------------------------------------------------------------------
		#Set PWM0 duty cycle to certain percentage
		#-----------------------------------------------------------------------
		self.PWM0_value =  duty_cycle * 256
		self.PWM0_value = int(math.floor(self.PWM0_value))
		self.bus.write_byte_data(self.address, self.__PWM0, self.PWM0_value) #set value
		time.sleep(0.005) #at least 500 microseconds required for set

	def setBlink2(self, blink_period=1, duty_cycle=0.05, frecuency=1):
		#-----------------------------------------------------------------------
		#Set pre-scaler PCS1 to dim at maximum frequency // Blink period = max = 0
		#-----------------------------------------------------------------------
		self.PSC1_value = blink_period * frecuency - 1
		self.PSC1_value = int(math.floor(self.PSC1_value))
		self.bus.write_byte_data(self.address, self.__PSC1, self.PSC1_value) #set value
		time.sleep(0.005) #at least 500 microseconds required for set

		#-----------------------------------------------------------------------
		#Set PWM1 duty cycle to certain percentage - dim value (1-0)
		#-----------------------------------------------------------------------
		self.PWM1_value =  duty_cycle * 256
		self.PWM1_value = int(math.floor(self.PWM1_value))
		self.bus.write_byte_data(self.address, self.__PWM1, self.PWM1_value) #set value
		time.sleep(0.005) #at least 500 microseconds required for set

	def updateInternalVal(self, light2, light1, fan, heater, debug):
		self.light2 = light2
		self.light1 = light1
		self.fan = fan
		self.heater = heater

		#Concatenate string and convert to hex
		#-----------------------------------------------------------------------
		self.val = self.light2 + self.light1 + self.fan + self.heater
		self.internal_val = int(self.val, 2)

		if debug:
			print ("Light2: ", self.light2)
			print ("Light1: ", self.light1)
			print ("Fan: ", self.fan)
			print ("Heater: ", self.heater)
			print ("Internal byte: ", self.val)
			print ("Decimal value: ", self.internal_val)

		#Assign PWMOutput to __LS0 reg
		#-----------------------------------------------------------------------    	
		self.bus.write_byte_data(self.address, self.__LS0, self.internal_val)
		time.sleep(0.005) #at least 500 microseconds required for set
	
	def getLighting1 (self):
		#Get value
		return str(self.status_light1)
		
	def setLighting1 (self, on = False, dimValue = 1, blink = False, debug = False):
		#Set value
		#-----------------------------------------------------------------------
		if on:
			if blink:
				#Set PWM0 output duty cycle
				self.setBlink1(1, 0.5, 152)
				
				#Associate light1 to PWM0
				self.light1 = "10"
				self.status_light1 = "BLINK"
				
			elif dimValue > 0:
				#Set PWM0 output duty cycle
				self.setBlink1(1, dimValue, 1)
				
				#Associate light1 to PWM0
				self.light1 = "10"
				self.status_light1 = "DIM%" + str(int(dimValue*100))
			else:
				self.light1 = "00"
				self.status_light1 = "ON"
		else:
			self.light1 = "01"
			self.status_light1 = "OFF"

		#Update value
		#-----------------------------------------------------------------------
		self.updateInternalVal(self.light2, self.light1, self.fan, self.heater, debug)		

	def getLighting2 (self):
		#Get value
		return self.status_light2
		
	def setLighting2 (self, on = False, dimValue = 1, blink = False, debug = False):
		#Set value
		#-----------------------------------------------------------------------
		if on:
			if blink:
				#Set PWM1 output duty cycle
				self.setBlink2(1, 0.5, 152)
				
				#Associate light1 to PWM1
				self.light2 = "11"
				self.status_light2 = "BLINK"
				
			elif dimValue > 0:
				#Set PWM1 output duty cycle
				self.setBlink2(1, dimValue, 1)
				
				#Associate light2 to PWM1		
				self.light2 = "11"
				self.status_light2 = "DIM%" + str(int(dimValue*100))
			else:
				self.light2 = "00"
				self.status_light2 = "ON"
		else:
			self.light2 = "01"
			self.status_light2 = "OFF"

		#Update value
		#-----------------------------------------------------------------------
		self.updateInternalVal(self.light2, self.light1, self.fan, self.heater, debug)		

	def getFan (self):
		#Get value
		return self.status_fan
		
	def setFan (self, on = False, debug = False):
		#Set value
		#-----------------------------------------------------------------------
		if on:
			self.fan = "00"
			self.status_fan = "ON"
		else:
			self.fan = "01"
			self.status_fan = "OFF"

		#Update value
		#-----------------------------------------------------------------------
		self.updateInternalVal(self.light2, self.light1, self.fan, self.heater, debug)		

	def getHeater (self):
		#Get value
		return self.status_heater
		
	def setHeater (self, on = False, debug = False):
		#Set value
		#-----------------------------------------------------------------------
		if on:
			self.heater = "00"
			self.status_heater = "ON"
		else:
			self.heater = "01"
			self.status_heater = "OFF"

		#Update value
		#-----------------------------------------------------------------------
		self.updateInternalVal(self.light2, self.light1, self.fan, self.heater, debug)		

	def showInfo (self):
		print ("----------------------------------------------------")
		print ("Status full device", self.bus.read_byte(self.address))
		print ("Status 0 - INPUT - input register =", self.bus.read_byte_data(self.address,self.__INPUT))
		print ("Status 1 - __PSC0 - frequency prescaler 0 =", self.bus.read_byte_data(self.address,self.__PSC0))
		print ("Status 2 - __PWM0 - PWM register 0 =", self.bus.read_byte_data(self.address,self.__PWM0))
		print ("Status 3 - __PSC1 - frequency prescaler 1 =", self.bus.read_byte_data(self.address,self.__PSC1))
		print ("Status 4 - __PWM1 - PWM register 1 =", self.bus.read_byte_data(self.address,self.__PWM1))
		print ("Status 5 - __LS0 - LED selector =", self.bus.read_byte_data(self.address,self.__LS0))
		print ("----------------------------------------------------")

if __name__ == "__main__":
	print ("----------------------------------------------------")
	print ("running - BUZZBOX test")
	print ("----------------------------------------------------")
	
	box = BuzzBox(1) 		#BUS 1

	#print ("Lighting set 1 ON")
	box.setLighting1 (True, 0, False)
	print "Lighting set 1 STATUS", box.getLighting1()
	time.sleep(5) 			#5 seconds wait

	#print ("Lighting set 1 BLINK")
	box.setLighting1 (True, 0, True)
	print "Lighting set 1 STATUS", box.getLighting1()
	time.sleep(5) 			

	#print ("Lighting set 1 DIMMABLE 50%")
	box.setLighting1 (True, 0.5, False)
	print "Lighting set 1 STATUS", box.getLighting1()
	time.sleep(5) 			

	#print ("Lighting set 2 ON")
	box.setLighting2 (True, 0, False)
	print "Lighting set 2 STATUS", box.getLighting2()
	time.sleep(5)

	#print ("Lighting set 2 BLINK")
	box.setLighting2 (True, 0, True)
	print "Lighting set 2 STATUS", box.getLighting2()
	time.sleep(5) 			

	#print ("Lighting set 2 DIMMABLE 5%")
	box.setLighting2 (True, 0.05, False)
	print "Lighting set 2 STATUS", box.getLighting2()
	time.sleep(5) 			

	#print ("Fan ON")
	box.setFan (True)
	print "Fan STATUS", box.getFan()
	time.sleep(2)

	#print ("Heater ON")
	box.setHeater (True)
	print "Heater STATUS", box.getHeater()
	time.sleep(2)

	#print ("Lighting set 1 OFF")
	box.setLighting1 (False, 0, False)
	print "Lighting set 1 STATUS", box.getLighting1()

	#print ("Lighting set 2 OFF")
	box.setLighting2 (False, 0, False)
	print "Lighting set 2 STATUS", box.getLighting2()

	#print ("Fan OFF")
	box.setFan (False)
	print "Fan STATUS", box.getFan()

	#print ("Heater OFF")
	box.setHeater (False)
	print "Heater STATUS", box.getHeater()

	print ("----------------------------------------------------")
	print("finished - BUZZBOX test")
	print ("----------------------------------------------------")