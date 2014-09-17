#-------------------------------------------------------------------------------
# Name:         motor_control_v2.py
# Purpose:      Control Fortito's BuzzBot
# Author:       Anasol Pena-Rios
# Created:      15/08/2013
# Copyright:    (c) FortiTo 2013
# Version:      1.0
#-------------------------------------------------------------------------------

import time
import motor
	
class MotorControl():

	#I2C Addresses
	#-------------------------------------------------------------------------------
	#Default bus is 0. To change the bus assign it when initialising the object
	#Bus to be use depends on the model of the Raspberry Pi	used

	#Global variables
	#-------------------------------------------------------------------------------
	servos = 0

	def __init__(self, busToUse = 0):
		# Initialise BUZZBOT
		self.servos = motor.Motor(1, 1, busToUse) # blink_period = 1, duty_cycle = 100%

		# Stop motors
		self.stopBot()
		#servos.showDebug ()

	def stopBot(self):
		# Stop motors
		self.servos.setDirection(0, self.servos.leftMotor)
		self.servos.setDirection(0, self.servos.rightMotor)

	def moveForward(self):
		self.servos.setDirection(1, self.servos.leftMotor)
		self.servos.setDirection(1, self.servos.rightMotor)
		#    time.sleep(0.9)

	def moveBackwards(self, on = True):
		self.servos.setDirection(-1, self.servos.leftMotor)
		self.servos.setDirection(-1, self.servos.rightMotor)
		#    time.sleep(0.9)		

	def turnLeft(self, init_step = -4, final_step = 4, debug = False):
		#Move within a range
		for i in range(init_step,final_step):
			if (debug):
				print ("LEFT MOTOR", -i)
				print ("RIGHT MOTOR", i)		
			self.servos.setDirection(i, self.servos.leftMotor)
			self.servos.setDirection(-i, self.servos.rightMotor)
			time.sleep(0.9)

	def turnRight(self, init_step = -4, final_step = 4, debug = False):
		#Move within a range
		for i in range(init_step,final_step):
			if (debug):
				print ("LEFT MOTOR", -i)
				print ("RIGHT MOTOR", i)			
			self.servos.setDirection(-i, self.servos.leftMotor)
			self.servos.setDirection(i, self.servos.rightMotor)
			time.sleep(0.9)

	def moveByStep(self, init_step = -5, final_step = 5, time_sleep = 0.9, debug = False):
		#Move within a range
		for i in range(init_step,final_step):
			if (debug):
				print ("LEFT MOTOR", -i)
				print ("RIGHT MOTOR", i)		
			self.servos.setDirection(i, self.servos.leftMotor)
			self.servos.setDirection(i, self.servos.rightMotor)
			time.sleep(time_sleep)

	def moveLeft(self, init_step = -4, final_step = 4, time_sleep = 0.9, debug = False):
		#Move within a range
		for i in range(init_step,final_step):
			if (debug):
				print ("LEFT MOTOR", -i)
				print ("RIGHT MOTOR", i)
			self.servos.setDirection(i, self.servos.leftMotor)
			self.servos.setDirection(-i, self.servos.rightMotor)
			time.sleep(time_sleep)

	def moveRight(self, init_step = -4, final_step = 4, time_sleep = 0.9, debug = False):
		#Move within a range
		for i in range(init_step,final_step):
			if (debug):
				print ("LEFT MOTOR", -i)
				print ("RIGHT MOTOR", i)
			self.servos.setDirection(-i, self.servos.leftMotor)
			self.servos.setDirection(i, self.servos.rightMotor)
			time.sleep(time_sleep)

if __name__ == "__main__":

	print ("----------------------------------------------------")
	print ("running MOTOR CONTROL test")
	print ("----------------------------------------------------")

	#Motor control
	#------------------------------------------------------------------------------
	try:
		bot = MotorControl(0)

		#Move forward
		for i in range(0,5):
			#print (i)
			bot.moveForward()
		#time.sleep(0.2)
		
		#Move backward
		for i in range(0,5):
			#print (i)
			bot.moveBackwards()
		#time.sleep(0.2)

		# Move robot, then stop
		bot.moveByStep(-2,0,0.02,True)
		#time.sleep(0.2)
		bot.moveRight (0,2,0.02,True)
		#time.sleep(0.2)
		bot.moveLeft (0,2,0.02,True)
		#bot.move_right (0,1,0.01)  ---THIS INSTRUCTION DOES NOT SEND ANY RESULT AS THE RANGE IS 0

		bot.stopBot()

	except Exception as e: 
		bot.stopBot()
		print "ERROR: MOTOR CONTROL - ", e

	print ("----------------------------------------------------")
	print("finished MOTOR CONTROL test")
	print ("----------------------------------------------------")
