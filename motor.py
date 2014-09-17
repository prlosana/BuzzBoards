#-------------------------------------------------------------------------------
# Name:         motor.py
# Purpose:      Use PCA9550 to control FortiTo's BuzzBot
#               PCA9550 - 2 selectable, fully programmable blink rates
#               (frequency and duty cycle)
#               between 0.172 Hz and 44 Hz (5.82 seconds and 0.023 second)
# Author:       Anasol Pena-Rios
# Created:      29/07/2013
# Copyright:    (c) FortiTo 2013
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time
import math

class Motor():

    #PIN DESCRIPTION
    #-------------------------------------------------------------------------------
    #Pin 1 = A0     - address input 0
    #Pin 2 = LED0   - LED driver 0
    #Pin 3 = LED1   - LED driver 1
    #Pin 4 = Vss    - supply ground
    #Pin 5 = RESET  - active LOW reset input
    #Pin 6 = SCL    - serial clock line (I2C)
    #Pin 7 = SDA    - serial data line  (I2C)
    #Pin 8 = Vdd    - supply voltage

    #I2C Addresses
    #-------------------------------------------------------------------------------
    #Default bus is 0. To change the bus assign it when initialising the object
    #Bus to be use depends on the model of the Raspberry Pi	used
    address     = 0x60              #PCA9550 address
    leftMotor   = 0x32              #address of the left motor
    rightMotor  = 0x33              #address of the right motor

    #Defining all subaddresses from Control Register Definition DataSheet
    #-------------------------------------------------------------------------------
    __INPUT  = 0x00      #Input register
    __PSC0   = 0x01      #prescaler 0
    __PWM0   = 0x02      #Pulse Width Modulator 0
    __PSC1   = 0x03      #prescaler 1
    __PWM1   = 0x04      #Pulse Width Modulator 1
    __LS0    = 0x05      #led selector
    frequency= 44        #Frecuencia en Hz

    #Global variables
    #-------------------------------------------------------------------------------
    bus = 0
    read_val = 0

    def __init__(self, blink_period=1, duty_cycle=0.5, busToUse = 0):
        # Initialise values
        self.bus = smbus.SMBus(busToUse) #open the bus on /dev/i2c-1

        #Values for the PWM
        #self.blink_period = blink_period
        #self.duty_cycle = duty_cycle

        #The following example will show how to set LED0 to blink at 1 Hz at a 50 % duty cycle
        #Set prescaler PSC0 to achieve a period of 1 second:
        #   __PSC0 = Blink period = 1 = (PSC0 + 1)/44
        #Set PWM0 duty cycle to 50 %:
        #   __PWM0 = (256 ? PWM0) / 256 = 0.5

        #-----------------------------------------------------------------------
        #Set prescaler PSC0 to achieve a certain blink period
        #-----------------------------------------------------------------------
        self.PSC0_value = blink_period * self.frequency - 1
        self.PSC0_value = int(math.floor(self.PSC0_value))
        self.bus.write_byte_data(self.address, self.__PSC0, self.PSC0_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

        #-----------------------------------------------------------------------
        #Set prescaler PSC1 to achieve a certain blink period
        #-----------------------------------------------------------------------
        self.PSC1_value = blink_period * self.frequency - 1
        self.PSC1_value = int(math.floor(self.PSC1_value))
        self.bus.write_byte_data(self.address, self.__PSC1, self.PSC1_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

        #-----------------------------------------------------------------------
        #Set PWM0 duty cycle to certain percentage
        #-----------------------------------------------------------------------
        self.PWM0_value =  256 - (duty_cycle * 256)
        self.PWM0_value = int(math.floor(self.PWM0_value))
        self.bus.write_byte_data(self.address, self.__PWM0, self.PWM0_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

        #-----------------------------------------------------------------------
        #Set PWM1 duty cycle to certain percentage
        #-----------------------------------------------------------------------
        self.PWM1_value =  256 - (duty_cycle * 256)
        self.PWM1_value = int(math.floor(self.PWM1_value))
        self.bus.write_byte_data(self.address, self.__PWM1, self.PWM1_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

    def setBlink0(self, blink_period=1, duty_cycle=0.5, frecuency=44):
    	
        #-----------------------------------------------------------------------
        #Set prescaler PSC0 to achieve a certain blink period
        #-----------------------------------------------------------------------
        self.PSC0_value = blink_period * frecuency - 1
        self.PSC0_value = int(math.floor(self.PSC0_value))
        self.bus.write_byte_data(self.address, self.__PSC0, self.PSC0_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

        #-----------------------------------------------------------------------
        #Set PWM0 duty cycle to certain percentage
        #-----------------------------------------------------------------------
        self.PWM0_value =  256 - (duty_cycle * 256)
        self.PWM0_value = int(math.floor(self.PWM0_value))
        self.bus.write_byte_data(self.address, self.__PWM0, self.PWM0_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

    def setBlink1(self, blink_period=1, duty_cycle=0.05, frecuency=1):

        #-----------------------------------------------------------------------
        #Set prescaler PCS1 to dim at maximum frequency // Blink period = max = 0
        #-----------------------------------------------------------------------
        self.PSC1_value = blink_period * frecuency - 1
        self.PSC1_value = int(math.floor(self.PSC1_value))
        self.bus.write_byte_data(self.address, self.__PSC1, self.PSC1_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set

        #-----------------------------------------------------------------------
        #Set PWM1 duty cycle to certain percentage - dim value (1-0)
        #-----------------------------------------------------------------------
        self.PWM1_value =  256 - (duty_cycle * 256)
        self.PWM1_value = int(math.floor(self.PWM1_value))
        self.bus.write_byte_data(self.address, self.__PWM1, self.PWM1_value) #set value
        time.sleep(0.005) #at least 500 microseconds required for set
		
    def showDebug (self):

        print ("----------------------------------------------------")
        print ("Status full device", self.bus.read_byte(self.address))
        print ("Status 0 - INPUT - input register =", self.bus.read_byte_data(self.address,self.__INPUT))
        print ("Status 1 - __PSC0 - frequency prescaler 0 =", self.bus.read_byte_data(self.address,self.__PSC0))
        print ("Status 2 - __PWM0 - PWM register 0 =", self.bus.read_byte_data(self.address,self.__PWM0))
        print ("Status 3 - __PSC1 - frequency prescaler 1 =", self.bus.read_byte_data(self.address,self.__PSC1))
        print ("Status 4 - __PWM1 - PWM register 1 =", self.bus.read_byte_data(self.address,self.__PWM1))
        print ("Status 5 - __LS0 - LED selector =", self.bus.read_byte_data(self.address,self.__LS0))
        print ("----------------------------------------------------")

    def setDirection(self, speed=0, motor=leftMotor):

        #PCA9550 does PWM out of 256 and servos take pulses with centre
        #around 1.5 ms with ~0.75ms either side
        #this function assumes frequency is at 44 Hz for servos expecting
        #pulses every 20ms

        #-------------------------------------------------------------------------------
        # Motor Type/Direction 2-bit: (default stepper/forward)
        #-------------------------------------------------------------------------------
        # Bit 0 controls the motor mode. If low the motor is in PWM mode and if high stepper mode.
        # Bit 1 controls motor direction. If low the motor moves the robot forward.
        # e.g. 0x00 - PWM/Forward
        # e.g. 0x02 - PWM/Backward

        #-------------------------------------------------------------------------------
        #PWM Motors:
        #-------------------------------------------------------------------------------
        # The motor speed is controlled by the PWM output of the MCU. If the PWM output is low
        # then power is applied to the motor. PWM0 (PA0) controls the left motor and PWM2 (PA2)
        # the right.

        #-----------------------------------------------------------------------
        #Assign the PWMOutput to __LS0 reg
        #-----------------------------------------------------------------------
        # LS0 (bits 7-4), LED1 (bits 3-2), LED0 (bits 1-0)
        # LS0 is always 1111
        # 00 = output is set LOW (LED on)
        # 01 = output is set high-impedance (LED off; default)
        # 10 = output blinks at PWM0 rate
        # 11 = output blinks at PWM1 rate
        # e.g. 11110110 (0xF6) - led1 is off and led0 blinks at PWM0 rate
        # e.g. 11111110 (0xFE) - led1 blinks at PWM1 rate and led0 blinks at PWM0 rate
        # e.g. 11110101 (0xF5) - LED off; default
        #-------------------------------------------------------------------------------

        if speed < 0:
            #print("Speed < 0",speed)
            #speed = -speed
            #-----------------------------------------------------------------------
            # Motor Type/Direction 2-bit: (PWM/Backward)
            #-----------------------------------------------------------------------
            self.bus.write_byte(motor,0x02)
            time.sleep(0.005) #at least 500 microseconds required for set
            #-----------------------------------------------------------------------
            #Set PWM0 output duty cycle - blink_period=1, duty_cycle=0.05 (Intensidad de la senal), frecuency=44 (periodo de tiempo en q manda la senal)
            #-----------------------------------------------------------------------
            self.setBlink0(1, 1, 44)
            self.setBlink1(1, 1, 44)
            #-----------------------------------------------------------------------
            #Assign the PWMOutput to __LS0 reg
            #-----------------------------------------------------------------------
            self.bus.write_byte_data(self.address, self.__LS0, 0xFE)
            time.sleep(0.005) #at least 500 microseconds required for set
        elif speed > 0:
            #print("Speed > 0",speed)
            #-----------------------------------------------------------------------
            # Motor Type/Direction: (PWM/forward)
            #-----------------------------------------------------------------------
            self.bus.write_byte(motor,0x00)
            time.sleep(0.005) #at least 500 microseconds required for set
            #-----------------------------------------------------------------------
            #Set PWM0 output duty cycle - blink_period=1, duty_cycle=0.05 (Intensidad de la senal), frecuency=44 (periodo de tiempo en q manda la senal)
            #-----------------------------------------------------------------------
            self.setBlink0(1, 1, 44)
            self.setBlink1(1, 1, 44)			
            #-----------------------------------------------------------------------
            #Assign the PWMOutput to __LS0 reg
            #-----------------------------------------------------------------------
            self.bus.write_byte_data(self.address, self.__LS0, 0xFE)
            time.sleep(0.005) #at least 500 microseconds required for set
        else:
            #print("Speed = 0",speed)
            #-----------------------------------------------------------------------
            #Assign the PWMOutput to __LS0 reg
            #-----------------------------------------------------------------------
            self.bus.write_byte_data(self.address, self.__LS0, 0xF5)
            time.sleep(0.005) #at least 500 microseconds required for set


if __name__ == "__main__":

    print ("----------------------------------------------------")
    print ("running - BUZZMOTOR test")
    print ("----------------------------------------------------")

    servos = Motor(1, 0.5, 0) # blink_period = 1, duty_cycle = 50%
    servos.setDirection(0, servos.leftMotor)
    servos.setDirection(0, servos.rightMotor)
    #servos.showDebug ()

    for i in range(-20,20):
        servos.setDirection(i, servos.leftMotor)
        #servos.showDebug ()
        servos.setDirection(i, servos.rightMotor)
        #servos.showDebug ()
        time.sleep(0.1)

    #while 1:
    servos.setDirection(0, servos.leftMotor)
    servos.setDirection(0, servos.rightMotor)

    print ("----------------------------------------------------")
    print("finished - BUZZMOTOR test")
    print ("----------------------------------------------------")
