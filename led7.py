#-------------------------------------------------------------------------------
# Name:         led7.py
# Purpose:      Use SAA1064 LED Driver to control FortiTo's Buzz-Led7
# Author:       Anasol Pena-Rios
# Created:      22/01/2013
# Copyright:    (c) FortiTo 2013
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time
import datetime

class led7():

    #I2C Addresses
    #-------------------------------------------------------------------------------
    bus         = smbus.SMBus(0)    #open the bus on /dev/i2c-0
    address     = 0x3b              #SAA1064 address

    #Defining all subaddresses from data_sheet Control register (page 6)
    # www.nxp.com/documents/data_sheet/SAA1064_CNV.pdf
    #-------------------------------------------------------------------------------
    __LEDS = [0x01, 0x02, 0x03, 0x04]
    __LED1  = 0x01      # Digit 1
    __LED2  = 0x02      # Digit 2
    __LED3  = 0x03      # Digit 3
    __LED4  = 0x04      # Digit 4

    def __init__(self):

        # Initialise display
        self.bus.write_byte_data(self.address,0x00,0x27)

    def clean(self):

        for x in self.__LEDS:
            self.bus.write_byte_data(self.address,x,0x00)

    def showValue(self, value="0000"):

        # Value to show on 7-segment led
        if len(value) == 0:
            for x in self.__LEDS:
                self.bus.write_byte_data(self.address,x,0x00)
        else:
            if len(value) > 4:
                value = value[:4]
            elif len(value) < 4:
                i = 4-len(value)
                for i in range(i):
                    value = "*" + value

            # Digit 1
            val = self.numToSeg(value[0])
            self.bus.write_byte_data(self.address,self.__LED1,val)

            # Digit 2
            val = self.numToSeg(value[1])
            self.bus.write_byte_data(self.address,self.__LED2,val)

            # Digit 3
            val = self.numToSeg(value[2])
            self.bus.write_byte_data(self.address,self.__LED3,val)

            # Digit 4
            val = self.numToSeg(value[3])
            self.bus.write_byte_data(self.address,self.__LED4,val)


    def numToSeg(self, val):

        # Equivalence to numbers on LED
        val = val.upper()
    	retval = 0x00; #default val

    	if val=="0":
    		retval = 0x3F
    	elif val=="1":
    		retval = 0x06
    	elif val=="2":
    		retval = 0x5B
    	elif val=="3":
    		retval = 0x4F
    	elif val=="4":
    		retval = 0x66
    	elif val=="5":
    		retval = 0x6D
    	elif val=="6":
    		retval = 0x7D
    	elif val=="7":
    		retval = 0x07
    	elif val=="8":
    		retval = 0x7F
    	elif val=="9":
    		retval = 0x6F
    	elif val== "A":
    		retval = 0x77
    	elif val== "B":
    		retval = 0x7C
    	elif val== "C":
    		retval = 0x39
    	elif val== "D":
    		retval = 0x5E
    	elif val== "E":
    		retval = 0x79
    	elif val== "F":
    		retval = 0x71
    	elif val== "G":
    		retval = 0x3D
    	elif val== "H":
    		retval = 0x76
    	elif val== "I":
    		retval = 0x30
    	elif val== "J":
    		retval = 0x1E
    	elif val== "L":
    		retval = 0x38
    	elif val== "N":
    		retval = 0x54
    	elif val== "O":
    		retval = 0x3F
    	elif val== "P":
    		retval = 0x73
    	elif val== "R":
    		retval = 0x50
    	elif val== "S":
    		retval = 0x6D
    	elif val== "T":
    		retval = 0x78
    	elif val== "U":
    		retval = 0x3E
    	elif val== "X":
    		retval = 0x76
    	elif val== "Y":
    		retval = 0x6E
    	elif val== "Z":
    		retval = 0x5B
    	elif val== "-":
    		retval = 0x40
    	elif val== "_":
    		retval = 0x08
    	elif val== ".":
    		retval = 0x80
        elif val=="*":
            retval = 0x00
        elif val=="":
            retval = 0x00
        else:
            retval = 0x27
    	return retval


    def showDebug (self, msg):

        print ("----------------------------------------------------")
        print ("Message: ", msg)
        print ("----------------------------------------------------")

if __name__ == "__main__":

    print ("----------------------------------------------------")
    print ("running BUZZLED7 test")
    print ("----------------------------------------------------")
    print ("Show current time...")

    # Obtain Time
    now = datetime.datetime.now()
    hour_str   = now.strftime("%H")
    minute_str = now.strftime("%M")
    msg = hour_str + minute_str

    # Messages on LED
    #msg = "err"
    #msg = "on"
    #msg = "off"
    #time.sleep(0.005) #500 microseconds

    display = led7()
    display.clean()
    display.showValue (msg)
    display.showDebug (msg)

    print ("----------------------------------------------------")
    print ("finished - BUZZLED7 test")
    print ("----------------------------------------------------")
