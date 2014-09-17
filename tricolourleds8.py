#-------------------------------------------------------------------------------
# Name:         tricolourleds8.py
# Purpose:      Use PCA8575 to control leds (8) for FortiTo's BuzzBot and BuzzBox
# Author:       Anasol Pena-Rios
# Created:      04/02/2014
# Copyright:    (c) FortiTo 2014
# Version:		1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class TricolourLeds8():

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used
	address_leds    = 0x23              #PCA8575 address

	#Attributes
	#-------------------------------------------------------------------------------
	status_led1 = "OFF"
	status_led2 = "OFF"
	status_led3 = "OFF"
	status_led4 = "OFF"
	status_led5 = "OFF"
	status_led6 = "OFF"
	status_led7 = "OFF"
	status_led8 = "OFF"

	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0
	all_green = 0x5555
	all_red = 0xAAAA
	all_yellow = 0x0000
	all_off = 0xFFFF
	l_yellow = "00"
	l_green = "01"
	l_red = "10"
	l_off = "11"
	yellow = "Y"
	red = "R"
	green = "G"
	off = "OFF"

	internal_val1 = 0
	val1 = "11111111"
	internal_val2 = 0
	val2 = "11111111"

	#Defining values from Control Register Definition DataSheet
	#-------------------------------------------------------------------------------
	led1 = "11"
	led2 = "11"
	led3 = "11"
	led4 = "11"
	led5 = "11"
	led6 = "11"
	led7 = "11"
	led8 = "11"

	def __init__(self, busToUse = 0):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1
		# Initialise leds
		self.bus.write_byte_data(self.address_leds,self.all_off,self.all_off)

	def updateInternalVal (self, debug):#(self, led1, led2, led3, led4, led5, led6, led7, led8, debug):
		#self.led1 = led1
		#self.led2 = led2
		#self.led3 = led3
		#self.led4 = led4
		#self.led5 = led5
		#self.led6 = led6
		#self.led7 = led7
		#self.led8 = led8

		#Concatenate string and convert to hex
		#-----------------------------------------------------------------------
		self.val1 = self.led4 + self.led3 + self.led2 + self.led1
		self.internal_val1 = int(self.val1, 2)

		self.val2 = self.led8 + self.led7 + self.led6 + self.led5
		self.internal_val2 = int(self.val2, 2)

		if debug:
			print ("led1: ", self.led1)
			print ("led2: ", self.led2)
			print ("led3: ", self.led3)
			print ("led4: ", self.led4)
			print ("Internal byte 1: ", self.val1)
			print ("Decimal value: ", self.internal_val1)
			print ("led8: ", self.led8)
			print ("led7: ", self.led7)
			print ("led6: ", self.led6)
			print ("led5: ", self.led5)
			print ("Internal byte 2: ", self.val2)
			print ("Decimal value: ", self.internal_val2)

		#Send value
		#-----------------------------------------------------------------------    	
		self.bus.write_byte_data(self.address_leds,self.internal_val1,self.internal_val2)
		time.sleep(0.005) #at least 500 microseconds required for set

	def clean(self):
		# Clean leds
		self.bus.write_byte_data(self.address_leds,self.all_off,self.all_off)
		self.status_led1 = self.off
		self.status_led2 = self.off
		self.status_led3 = self.off
		self.status_led4 = self.off
		self.status_led5 = self.off
		self.status_led6 = self.off
		self.status_led7 = self.off
		self.status_led8 = self.off

	def turnOnAllRed(self):
		self.bus.write_byte_data(self.address_leds,self.all_red,self.all_red)
		self.status_led1 = self.red
		self.status_led2 = self.red
		self.status_led3 = self.red
		self.status_led4 = self.red
		self.status_led5 = self.red
		self.status_led6 = self.red
		self.status_led7 = self.red
		self.status_led8 = self.red

	def turnOnAllGreen(self):
		self.bus.write_byte_data(self.address_leds,self.all_green,self.all_green)
		self.status_led1 = self.green
		self.status_led2 = self.green
		self.status_led3 = self.green
		self.status_led4 = self.green
		self.status_led5 = self.green
		self.status_led6 = self.green
		self.status_led7 = self.green
		self.status_led8 = self.green

	def turnOnAllYellow(self):
		self.bus.write_byte_data(self.address_leds,self.all_yellow,self.all_yellow)
		self.status_led1 = self.yellow
		self.status_led2 = self.yellow
		self.status_led3 = self.yellow
		self.status_led4 = self.yellow
		self.status_led5 = self.yellow
		self.status_led6 = self.yellow
		self.status_led7 = self.yellow
		self.status_led8 = self.yellow

	def getLed1 (self):
		#Get value
		return str(self.status_led1)

	def getLed2 (self):
		#Get value
		return str(self.status_led2)

	def getLed3 (self):
		#Get value
		return str(self.status_led3)

	def getLed4 (self):
		#Get value
		return str(self.status_led4)

	def getLed5 (self):
		#Get value
		return str(self.status_led5)

	def getLed6 (self):
		#Get value
		return str(self.status_led6)

	def getLed7 (self):
		#Get value
		return str(self.status_led7)

	def getLed8 (self):
		#Get value
		return str(self.status_led8)

	def turnOnLed(self, led = 0, colour = 0, debug=False):
		# Colour code: 0=yellow, 1=green, 2=red, 3=off
		if led == 1:
			if colour == 0:	# yellow
				self.led1 = self.l_yellow
				self.status_led1 = self.yellow
			elif colour == 1:	# green
				self.led1 = self.l_green
				self.status_led1 = self.green
			elif colour == 2:	# red
				self.led1 = self.l_red
				self.status_led1 = self.red
			elif colour == 3:	# off
				self.led1 = self.l_off
				self.status_led1 = self.off
		elif led == 2:
			if colour == 0:	# yellow
				self.led2 = self.l_yellow
				self.status_led2 = self.yellow
			elif colour == 1:	# green
				self.led2 = self.l_green
				self.status_led2 = self.green
			elif colour == 2:	# red
				self.led2 = self.l_red
				self.status_led2 = self.red
			elif colour == 3:	# off
				self.led2 = self.l_off
				self.status_led2 = self.off
		elif led == 3:
			if colour == 0:	# yellow
				self.led3 = self.l_yellow
				self.status_led3 = self.yellow
			elif colour == 1:	# green
				self.led3 = self.l_green
				self.status_led3 = self.green
			elif colour == 2:	# red
				self.led3 = self.l_red
				self.status_led3 = self.red
			elif colour == 3:	# off
				self.led3 = self.l_off
				self.status_led3 = self.off
		elif led == 4:
			if colour == 0:	# yellow
				self.led4 = self.l_yellow
				self.status_led4 = self.yellow
			elif colour == 1:	# green
				self.led4 = self.l_green
				self.status_led4 = self.green
			elif colour == 2:	# red
				self.led4 = self.l_red
				self.status_led4 = self.red
			elif colour == 3:	# off
				self.led4 = self.l_off
				self.status_led4 = self.off
		elif led == 5:
			if colour == 0:	# yellow
				self.led5 = self.l_yellow
				self.status_led5 = self.yellow
			elif colour == 1:	# green
				self.led5 = self.l_green
				self.status_led5 = self.green
			elif colour == 2:	# red
				self.led5 = self.l_red
				self.status_led5 = self.red
			elif colour == 3:	# off
				self.led5 = self.l_off
				self.status_led5 = self.off
		elif led == 6:
			if colour == 0:	# yellow
				self.led6 = self.l_yellow
				self.status_led6 = self.yellow
			elif colour == 1:	# green
				self.led6 = self.l_green
				self.status_led6 = self.green
			elif colour == 2:	# red
				self.led6 = self.l_red
				self.status_led6 = self.red
			elif colour == 3:	# off
				self.led6 = self.l_off
				self.status_led6 = self.off
		elif led == 7:
			if colour == 0:	# yellow
				self.led7 = self.l_yellow
				self.status_led7 = self.yellow
			elif colour == 1:	# green
				self.led7 = self.l_green
				self.status_led7 = self.green
			elif colour == 2:	# red
				self.led7 = self.l_red
				self.status_led7 = self.red
			elif colour == 3:	# off
				self.led7 = self.l_off
				self.status_led7 = self.off
		elif led == 8:
			if colour == 0:	# yellow
				self.led8 = self.l_yellow
				self.status_led8 = self.yellow
			elif colour == 1:	# green
				self.led8 = self.l_green
				self.status_led8 = self.green
			elif colour == 2:	# red
				self.led8 = self.l_red
				self.status_led8 = self.red
			elif colour == 3:	# off
				self.led8 = self.l_off
				self.status_led8 = self.off

		#Update value
		#-----------------------------------------------------------------------
		self.updateInternalVal(debug)	

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running TRICOLOURLEDS8 test")
	print ("----------------------------------------------------")

	tricolor = TricolourLeds8(1)
	tricolor.clean()
	tricolor.turnOnLed (1,0)
	print "Led 1 STATUS ", tricolor.getLed1()	
	time.sleep(1)
	tricolor.turnOnLed (2,1)
	print "Led 2 STATUS ", tricolor.getLed2()	
	time.sleep(1)
	tricolor.turnOnLed (3,2)
	print "Led 3 STATUS ", tricolor.getLed3()	
	time.sleep(1)
	tricolor.turnOnLed (4,0)
	print "Led 4 STATUS ", tricolor.getLed4()	
	time.sleep(1)
	tricolor.turnOnLed (5,1)
	print "Led 5 STATUS ", tricolor.getLed5()	
	time.sleep(1)
	tricolor.turnOnLed (6,2)
	print "Led 6 STATUS ", tricolor.getLed6()	
	time.sleep(1)
	tricolor.turnOnLed (7,0)
	print "Led 7 STATUS ", tricolor.getLed7()	
	time.sleep(1)
	tricolor.turnOnLed (8,1)
	print "Led 8 STATUS ", tricolor.getLed8()	
	time.sleep(1)
	tricolor.turnOnAllYellow()
	print "Led 1 STATUS ", tricolor.getLed1()	
	time.sleep(1)
	tricolor.turnOnAllGreen()
	print "Led 2 STATUS ", tricolor.getLed2()	
	time.sleep(1)
	tricolor.turnOnAllRed()
	print "Led 3 STATUS ", tricolor.getLed3()	
	time.sleep(1)
	tricolor.clean()

	print ("----------------------------------------------------")
	print ("finished - TRICOLOURLEDS8 test")
	print ("----------------------------------------------------")
