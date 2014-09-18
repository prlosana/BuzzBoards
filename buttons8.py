#-------------------------------------------------------------------------------
# Name:         buttons8.py
# Purpose:      Use PCA8575 to control buttons (8) for FortiTo's BuzzBot and BuzzBox
# Author:       Anasol Pena-Rios
# Created:      24/01/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time 

class buttons8():

    #I2C Addresses
    #-------------------------------------------------------------------------------
    address_buttons	= 0x22              #PCA8575 address

    #Attributes
    #-------------------------------------------------------------------------------
    status_btn1 = "OFF"
    status_btn2 = "OFF"
    status_btn3 = "OFF"
    status_btn4 = "OFF"
    status_btn5 = "OFF"
    status_btn6 = "OFF"
    status_btn7 = "OFF"
    status_btn8 = "OFF"
    
	#Global variables
	#-------------------------------------------------------------------------------
	bus = 0
    read_val = 255

	def __init__(self, busToUse = 0):
		# Initialise values
		self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1
        self.read_val = 255
	
    def clean(self):
		# Clean values
		self.read_val = 255

    def readValue(self, debug = False):
		# Read values - Default value 255 (0xFF)
		self.read_val = self.bus.read_byte(self.address_buttons)	
		msg = ""
		time.sleep(0.2) #0.2 second
		
		if self.read_val <> 255:
			# Evaluate value
			if self.read_val==254: # 0xFE
				self.read_val = 255	
				if self.status_btn1 == "OFF":
					self.status_btn1 = "ON"
				else:
					self.status_btn1 = "OFF"
				msg = "BTN1_"+self.status_btn1
			elif self.read_val==253: # 0xFD
				self.read_val = 255			
				if self.status_btn2 == "OFF":
					self.status_btn2 = "ON"
				else:
					self.status_btn2 = "OFF"
				msg = "BTN2_"+self.status_btn2
			elif self.read_val==251: # 0xFB
				self.read_val = 255			
				if self.status_btn3 == "OFF":
					self.status_btn3 = "ON"
				else:
					self.status_btn3 = "OFF"
				msg = "BTN3_"+self.status_btn3
			elif self.read_val==247: # 0xF7
				self.read_val = 255			
				if self.status_btn4 == "OFF":
					self.status_btn4 = "ON"
				else:
					self.status_btn4 = "OFF"
				msg = "BTN4_"+self.status_btn4	
			elif self.read_val==239: # 0xEF
				self.read_val = 255			
				if self.status_btn5 == "OFF":
					self.status_btn5 = "ON"
				else:
					self.status_btn5 = "OFF"
				msg = "BTN5_"+self.status_btn5
			elif self.read_val==223: # 0xDF
				self.read_val = 255			
				if self.status_btn6 == "OFF":
					self.status_btn6 = "ON"
				else:
					self.status_btn6 = "OFF"
				msg = "BTN6_"+self.status_btn6	
			elif self.read_val==191: # 0xBF
				self.read_val = 255			
				if self.status_btn7 == "OFF":
					self.status_btn7 = "ON"
				else:
					self.status_btn7 = "OFF"
				msg = "BTN7_"+self.status_btn7	
			elif self.read_val==127: # 0x7F
				self.read_val = 255			
				if self.status_btn8 == "OFF":
					self.status_btn8 = "ON"
				else:
					self.status_btn8 = "OFF"
				msg = "BTN8_"+self.status_btn8
			
			if debug:
				print msg, " pressed."
				
		return msg

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running BUTTONS8 test")
	print ("----------------------------------------------------")
	
	print ("Press a button...")
	result = ""
	buttons = buttons8()
	buttons.clean()

	while 1:
		result = buttons.readValue (True)
		if result <> "":
			print "Result = ", result
			result = ""

	print ("----------------------------------------------------")
	print ("finished - BUTTONS8 test")
	print ("----------------------------------------------------")
