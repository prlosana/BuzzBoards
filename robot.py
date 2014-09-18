#-------------------------------------------------------------------------------
# Name:         robot.py
# Purpose:      Demonstration of FortiTo's BuzzBoard
# Author:       Anasol Pena-Rios
# Created:      30/07/2013
# Copyright:    (c) FortiTo 2013
# Version:      1.0
#-------------------------------------------------------------------------------

import smbus
import time
import datetime
import motorControl
import led7

class robot():

    def __init__(self):
        # Initialise display
        print ("----------------------------------------------------")


if __name__ == "__main__":

    # Access the i2c bus
    bus = smbus.SMBus(0)

    #----UR RANGERS-------
    # Address of the device (i2cdetect -y 0)
    # Send value to physical address
    # bus.write_byte_data(0x6c, 0, 0x51)
    # print "UR_Ranger 0x6c, raw value::", bus.read_word_data(0x6c, 2)/255
    # bus.write_byte_data(0x6d, 0, 81)
    # print "UR_Ranger 0x6d, raw value::", bus.read_word_data(0x6d, 2)/255

    #----IR RANGERS-------
    # Address of the device (i2cdetect -y 0)
    # bus.frequency(16000)
    # Enable IR Ranger
    # bus.write_byte_data(0x28, 0x00, 0x01)
    # Send value to physical address
    print "IR_Ranger 0x28 - front left left:", 3.3 / 255.0 * bus.read_byte(0x28)
    print "IR_Ranger 0x29 - front left front:", 3.3 / 255.0 * bus.read_byte(0x29)
    print "IR_Ranger 0x2A - front right front:", 3.3 / 255.0 * bus.read_byte(0x2a)
    time.sleep(0.04)
    print "IR_Ranger 0x2B - front right right:", bus.read_byte(0x2b)
    print "IR_Ranger 0x2C - back right right:", 5 / 255.0 * bus.read_byte(0x2c)
    print "IR_Ranger 0x2D - back right back:", 3.3 / 255.0 * bus.read_byte(0x2d)
    print "IR_Ranger 0x2E - back left back:", 3.3 / 255.0 * bus.read_byte(0x2e)
    print "IR_Ranger 0x2F - back left left:", 3.3 / 255.0 * bus.read_byte(0x2f)

    #----LINE FOLLOWER-------
    # Address of the device (i2cdetect -y 0)
    # Send value to physical address
    print "Line follower 0x30, raw value:", bus.read_byte(0x30)

    #----LIGHT SENSORS-------
    # Adress of the device (i2cdetect -y 0)
    # Send value to physical address
    print "Light sensor 0x31, raw value:", bus.read_byte(0x31)

    #-------------------
    #----BUZZLED7------
    #-------------------
    # Obtain Time
    now = datetime.datetime.now()
    hour_str   = now.strftime("%H")
    minute_str = now.strftime("%M")
    print "Hour: " + hour_str + " Minute: " + minute_str

    # Messages on LED
    msg = hour_str[0] + hour_str[1] + minute_str[0] + minute_str[1]
    display = led7.led7()
    display.clean()
    display.showValue (msg)
    #display.showDebug (msg)

    #-------------------
    #-----BUZZBOT-------
    #-------------------
    bot = motorControl.motorControl()
    bot.stopBot()

    # Move forward and backwards, then stop
    bot.moveByStep(-2,2)
    print ("Move by step")

    # Move continuously
    #bot.moveForward(True)
    #bot.moveBackwards(True)
    bot.stopBot()