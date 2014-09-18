#-------------------------------------------------------------------------------
# Name:         fortitoServer.py
# Purpose:      Socket to connect to FortiTo's BuzzBox functions
# Author:       Anasol Pena-Rios
# Created:      15/04/2014
# Copyright:    (c) FortiTo 2014
# Version:      1.0
#-------------------------------------------------------------------------------

import time
import pygame
import buzzbox
import tricolourleds8
import buttons8
import wear_multiplexer
import wear_multiplexer_reader
import wear_sensor_heat
import wear_sensor_light
import wear_sensor_motion
import motorControl
#import led7
import socket
import select
import sys
import Queue
import threading

#Global variables
#-------------------------------------------------------------------------------
i2cBus = 0	#This depends on the model of the Raspberry Pi		 
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 50000	# Arbitrary non-privileged port
HOST1 = '192.168.1.20' #'155.245.23.119'
PORT1 = 50001
s = None
connected = False
msg = ""
exitFlag = 0

connected_client_buttons = False
connected_multiplexer = False
connected_sensor_light = False
connected_sensor_temp = False
connected_sensor_motion = False
current_channel = 0

btn_result = ""
messages = []
size = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
		print "Starting " + self.name
		sendButtonStatus()
		print "Exiting " + self.name

# Define a functions for the thread
def sendButtonStatus():
	global size
	global HOST1
	global PORT1
	global messages
	s = None
	global connected_client_buttons

	print "Start socket button status..."

	# Infinite loop
	while 1:	
		#if exitFlag: return	-ACPR to work with assignments	
		
		size = len(messages)
		#print 'SIZE = ', size
		
		#if messages:
		#for message in messages:
		while messages:
			#if exitFlag: return	-ACPR to work with assignments		
			try:
				if not connected_client_buttons:
					# Create a TCP/IP socket
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					print 'connecting to ', HOST1, ' port ', PORT1	

					#for s in socks:
					s.settimeout(5)  #Wait for 5 seconds
					s.connect((HOST1, PORT1))
					#s.create_connection((HOST1, PORT1))
					connected_client_buttons = True
					print 'Connected!'
					s.settimeout(None)	

				if connected_client_buttons:
					while messages:
						#Remove it from the list
						msg = messages.pop(0)

						msg = msg+"\n"
						# Send messages on socket
						s.send(msg)
						print '%s: sending item "%s"' % (s.getsockname(), msg)

						# Read responses on socket
						data = s.recv(1024)
						if data == "":
							data = "No acknowledge message from the server."
						
						print '%s: received "%s"' % (s.getsockname(), data)
						
						#s.sendall()
						
					s.close()
					connected_client_buttons = False
					
			except socket.timeout:
				print "Time out when connecting to ", HOST1, " port ", PORT1
				del messages[:]
				connected_client_buttons = False
				continue
			   
			except socket.error as msg:
				s = None
				print "ERROR: Socket error! %s" % msg
				connected_client_buttons = False
				'''
				if "Errno 104" in msg:
					connected_client_buttons = False
					continue
				else:
				'''
				#break
				continue
				
			except KeyboardInterrupt:
				print "Socket stopped..."	
				if connected_client_buttons: s.close()	
				break

			except:
				print "ERROR: Unexpected error:", sys.exc_info()[0]	
				break				
	   
class buttonsThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
		print "Starting " + self.name
		getButtons()
		print "Exiting " + self.name

# Define a functions for the thread
def getButtons():
	result = ""
	#Creates buttons instance
	buttons = buttons8.Buttons8(i2cBus)
	buttons.clean()

	print "Start buttons listening..."
	
	while True:
		#if exitFlag: return -ACPR to work with assignments	
			
		result = buttons.readValue()
		if result <> "":
			global btn_result
			global messages
			btn_result = str(result)
			#if connected_client_buttons:
			#	print btn_result, " pressed - Connected.............."
			print btn_result, " pressed.............."
			messages.append(btn_result)
			#else:
			#	print btn_result, " pressed - Not connected.........."
			#	messages.append(btn_result)
			result = ""

class sensorDiscoveryServiceThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
		print "Starting " + self.name
		sensorDiscoveryService()
		print "Exiting " + self.name

# Define functions for the thread
def sensorDiscoveryService():
	global i2cBus	
	global connected_multiplexer
	global connected_sensor_light
	global connected_sensor_temp
	global connected_sensor_motion
	
	print "Start sensor discovery service..."
	
	while True:
		if exitFlag: return
			
		#Enable multiplexer
		try:
			while (not connected_multiplexer):
				result = ""
				multiplexer = wear_multiplexer.WearMultiplexer(i2cBus)
				connected_multiplexer = True

			if (connected_sensor_temp or connected_sensor_light or connected_sensor_motion):
				pass
				#print "MULTIPLEXER - Device(s) connected"
			else:
				for channel in range(1,17):
					if (connected_multiplexer):
						#Select channel
						try:
							result = multiplexer.setChannel(channel)
							print "MULTIPLEXER - Enabling channel ",channel," in the board... ", result
							
							current_channel = channel
							
							if (not connected_sensor_temp):
								try:
									#Start temperature sensor
									temperatureSensor = wear_sensor_heat.WearSensorHeat(i2cBus)

									#Set precision
									decimals = 4
									result = temperatureSensor.setPrecision(decimals)
					
									connected_sensor_temp = True
									
								except Exception as e: 
									#print "ERROR: HEAT SENSOR - ", e		
									connected_sensor_temp = False

							if (not connected_sensor_light):
								try:
									#Start light sensor
									lightSensor = wear_sensor_light.WearSensorLight(i2cBus)
								
									connected_sensor_light = True
									
								except Exception as e: 	
									#print "ERROR: LIGHT SENSOR - ", e
									connected_sensor_light = False
								
							if (not connected_sensor_motion):
								try:
									#Start motion sensor
									motionSensor = wear_sensor_motion.WearSensorMotion(bus)
								
									connected_sensor_motion = True
									
								except Exception as e: 	
									#print "ERROR: MOTION SENSOR - ", e
									connected_sensor_motion = False
										
							if (connected_sensor_temp or connected_sensor_light or connected_sensor_motion):
								break
								
						except Exception as e: 
							pass
							#print "ERROR: MULTIPLEXER - ", e		
					else:
						break

			#Start reading sensors
			if (connected_sensor_temp):
				try:
					result = temperatureSensor.getTemperature()		
					#print "HEAT SENSOR - Temperature ", result, " C"
				except Exception as e: 
					print "ERROR: HEAT SENSOR - ", e		
					connected_sensor_temp = False
			
			if (connected_sensor_light):
				try: 
					result = lightSensor.getLux()
					#print "LIGHT SENSOR - Lux ", result						
				except Exception as e: 	
					print "ERROR: LIGHT SENSOR - ", e
					connected_sensor_light = False

			if (connected_sensor_motion):
				try: 
					x = motionSensor.getXAxis()		
					y = motionSensor.getYAxis()		
					z = motionSensor.getZAxis()	
					print "MOTION SENSOR - X=", x, ", Y=", y, ", Z=", z						
				except Exception as e: 	
					print "ERROR: MOTION SENSOR - ", e
					connected_sensor_motion = False
					
		except Exception as e: 
			#print "ERROR: MULTIPLEXER - ", e		
			connected_multiplexer = False

#Start main program		
if __name__ == "__main__":
				
	# Create new threads
	try:
		thread1 = sensorDiscoveryServiceThread(1, "Thread1 - Sensor Discovery Service")
		thread1.start()
	except:
	   print "ERROR: unable to start threads", sys.exc_info()[0]	
	   exitFlag = 1

	try:
		thread2 = buttonsThread(1, "Thread2 - Buttons")
		thread2.start()
	except:
	   print "ERROR: unable to start threads", sys.exc_info()[0]	
	   exitFlag = 1

	try:
		thread3 = myThread(1, "Thread3 - Send Button status")
		thread3.start()
	except:
	   print "ERROR: unable to start threads", sys.exc_info()[0]	
	   exitFlag = 1
	   
	#Creates box instance
	try: 
		box = buzzbox.BuzzBox(i2cBus)
		box.clean()
	except Exception as e: 
		print "ERROR: BUZZBOX Unexpected error:", e #sys.exc_info()[0]
		#exitFlag = 1
		
	#Creates tricolour leds instance
	try: 
		# Colour code: 0=yellow, 1=green, 2=red, 3=off
		tricolor = tricolourleds8.TricolourLeds8(i2cBus)
		tricolor.clean()		
	except Exception as e: 
		print "ERROR: TRICOLOUR LEDS Unexpected error:", e
		#exitFlag = 1
	
	"""
	try: 
		# Creates instances 7-segment display
		display = led7.led7()
		display.clean()
	except Exception as e: 
		print "ERROR: 7-SEGMENT DISPLAY Unexpected error:", e #sys.exc_info()[0]
		#exitFlag = 1		
	"""	
	try: 
		# Creates instances robot
		bot = motorControl.MotorControl(i2cBus)
		bot.stopBot()
	except Exception as e: 
		print "ERROR: BOT Unexpected error:", e
		#exitFlag = 1
	
	try:
		# Create a TCP/IP socket
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setblocking(0)
	except socket.error as msg:
		server = None
		print "ERROR: Create socket %s" % msg
		
	try:
		# Bind it to TCP address and port
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
		server.bind((HOST, PORT))
		print 'Starting up on ', HOST, ' port ', PORT		
	except socket.error as msg:
		server.close()
		print 'ERROR: Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		server = None
		
	if server is None:
		print 'could not open socket'
		# Notify threads it's time to exit
		#exitFlag = 1
		sys.exit(1)

	try:
		# Infinite loop
		while 1:	
			#print "MULTIPLEXER - Current channel selected ",current_channel
		
			# Listen for incoming connections
			server.listen(5)
			print 'Server started and listening'

			# Sockets from which we expect to read
			inputs = [ server ]

			# Sockets to which we expect to write
			outputs = [ ]

			# Outgoing message queues (socket:Queue)
			message_queues = {}

			try:		
				while inputs:
					# Wait for at least one of the sockets to be ready for processing
					print 'waiting for the next event'
					readable, writable, exceptional = select.select(inputs, outputs, inputs)
					
					# Handle inputs
					for s in readable:

						if s is server:
							# A "readable" server socket is ready to accept a connection
							connection, client_address = s.accept()
							print 'new connection from', client_address
							connection.setblocking(0)
							inputs.append(connection)
					
							connected = True

							# Give the connection a queue for data we want to send
							message_queues[connection] = Queue.Queue()
								
						else:					
							# Receive data
							data = connection.recv(1024).decode()
									
							if data:
								#A readable client socket has data
								print 'received "%s" from %s' % (data, s.getpeername())
							
								#Evaluates data
								data = data.upper()
								print (data)
								msg = "OK"
								
								subdata_pos = data.find("%")
								subdata = data[0:subdata_pos]
								subvalue = 0
								#print "character % found at ", subdata_pos, " command ", subdata

								subdata1_pos = data.find("&")
								subdata1 = data[0:subdata1_pos]
								subvalue1 = 0
								if data == "HELLO\n":
									HOST1 = str(client_address[0])
									print "Buttons host = ", HOST1
								elif data == "PLAY1\n":
									pygame.mixer.init()
									pygame.mixer.music.load("/home/pi/BuzzBoards/music1.mp3")
									pygame.mixer.music.play()
								elif data == "PLAY2\n":
									pygame.mixer.init()
									pygame.mixer.music.load("/home/pi/BuzzBoards/music2.mp3")
									pygame.mixer.music.play()
								elif data == "STOP\n":
									pygame.mixer.stop()
									pygame.mixer.music.stop()
									pygame.mixer.quit()
								elif data == "LIGHT1_ON\n":			 
									print ("Lighting set 1 ON")
									box.setLighting1 (True, 0, False)
									time.sleep(1) 
								elif data == "LIGHT1_BLINK\n":
									print ("Lighting set 1 BLINK")
									box.setLighting1 (True, 0, True)
									time.sleep(1) 			
								elif subdata == "LIGHT1_DIM":  #format for dimmable values LIGHT1_DIM%5
									try:
										subvalue = float (data[subdata_pos+1:])
									except ValueError:
										msg = "ERROR: INVALID DIM VALUE"
										subvalue = 0
									#print "subvalue=", subvalue
									if subvalue > 100 or subvalue < 0:
										msg = "ERROR: VALUE OUT OF RANGE"			
										print ("Lighting set 1 DIMMABLE", msg)			
									else:
										dim = float(subvalue / 100)
										print ("Lighting set 1 DIMMABLE ", subvalue , " % - ", dim)
										box.setLighting1 (True, dim, False)
										time.sleep(1) 			
								elif data == "GET_LIGHT1\n":
									msg = box.getLighting1()
									print ("Lighting set 1  - Get status ",msg)
									time.sleep(1)		
								elif data == "LIGHT2_ON\n":
									print ("Lighting set 2 ON")
									box.setLighting2 (True, 0, False)
									time.sleep(1)
								elif data == "LIGHT2_BLINK\n":
									print ("Lighting set 2 BLINK")
									box.setLighting2 (True, 0, True)
									time.sleep(1) 			
								elif subdata == "LIGHT2_DIM":  #format for dimmable values LIGHT1_DIM%5
									try:
										subvalue = float (data[subdata_pos+1:])
									except ValueError:
										msg = "ERROR: INVALID DIM VALUE"
										subvalue = 0
									#print "subvalue=", subvalue
									if subvalue > 100 or subvalue < 0:
										msg = "ERROR: VALUE OUT OF RANGE"			
										print ("Lighting set 2 DIMMABLE", msg)			
									else:
										dim = float(subvalue / 100)
										print ("Lighting set 2 DIMMABLE ", subvalue , " % - ", dim)
										box.setLighting2 (True, dim, False)
										time.sleep(1) 			
								elif data == "GET_LIGHT2\n":
									msg = box.getLighting2()
									print ("Lighting set 2  - Get status ",msg)
									time.sleep(1)		
								elif data == "FAN_ON\n":
									print ("Fan ON")
									box.setFan (True)
									time.sleep(1)
								elif data == "HEATER_ON\n":
									print ("Heater ON")
									box.setHeater (True)
									time.sleep(1)
								elif data == "LIGHT1_OFF\n":
									print ("Lighting set 1 OFF")
									box.setLighting1 (False, 0, False)
									time.sleep(1)
								elif data == "LIGHT2_OFF\n":
									print ("Lighting set 2 OFF")
									box.setLighting2 (False, 0, False)
									time.sleep(1)
								elif data == "FAN_OFF\n":
									print ("Fan OFF")
									box.setFan (False)
									time.sleep(1)
								elif data == "HEATER_OFF\n":
									print ("Heater OFF")
									box.setHeater (False)
									time.sleep(1)
								elif data == "GET_FAN\n":
									msg = box.getFan()
									print ("Fan  - Get status ",msg)
									time.sleep(1)		
								elif data == "GET_HEATER\n":
									msg = box.getHeater()
									print ("Heater  - Get status ",msg)
									time.sleep(1)	
								elif data == "GET_LED1\n":
									msg = tricolor.getLed1()
									print ("Led 1  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED2\n":
									msg = tricolor.getLed2()
									print ("Led 2  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED3\n":
									msg = tricolor.getLed3()
									print ("Led 3  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED4\n":
									msg = tricolor.getLed4()
									print ("Led 4  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED5\n":
									msg = tricolor.getLed5()
									print ("Led 5  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED6\n":
									msg = tricolor.getLed6()
									print ("Led 6  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED7\n":
									msg = tricolor.getLed7()
									print ("Led 7  - Get status ",msg)
									time.sleep(1)
								elif data == "GET_LED8\n":
									msg = tricolor.getLed8()
									print ("Led 8  - Get status ",msg)
									time.sleep(1)									
								elif data == "LED1_R\n":
									print ("Led 1 RED")
									tricolor.turnOnLed (1,2)
									time.sleep(1)
								elif data == "LED1_G\n":
									print ("Led 1 GREEN")
									tricolor.turnOnLed (1,1)
									time.sleep(1)
								elif data == "LED1_Y\n":
									print ("Led 1 YELLOW")
									tricolor.turnOnLed (1,0)
									time.sleep(1)
								elif data == "LED1_OFF\n":
									print ("Led 1 OFF")
									tricolor.turnOnLed (1,3)
									time.sleep(1)
								elif data == "LED2_R\n":
									print ("Led 2 RED")
									tricolor.turnOnLed (2,2)
									time.sleep(1)
								elif data == "LED2_G\n":
									print ("Led 2 GREEN")
									tricolor.turnOnLed (2,1)
									time.sleep(1)
								elif data == "LED2_Y\n":
									print ("Led 2 YELLOW")
									tricolor.turnOnLed (2,0)
									time.sleep(1)
								elif data == "LED2_OFF\n":
									print ("Led 2 OFF")
									tricolor.turnOnLed (2,3)
									time.sleep(1)
								elif data == "LED3_R\n":
									print ("Led 3 RED")
									tricolor.turnOnLed (3,2)
									time.sleep(1)
								elif data == "LED3_G\n":
									print ("Led 3 GREEN")
									tricolor.turnOnLed (3,1)
									time.sleep(1)
								elif data == "LED3_Y\n":
									print ("Led 3 YELLOW")
									tricolor.turnOnLed (3,0)
									time.sleep(1)
								elif data == "LED3_OFF\n":
									print ("Led 3 OFF")
									tricolor.turnOnLed (3,3)
									time.sleep(1)
								elif data == "LED4_R\n":
									print ("Led 4 RED")
									tricolor.turnOnLed (4,2)
									time.sleep(1)
								elif data == "LED4_G\n":
									print ("Led 4 GREEN")
									tricolor.turnOnLed (4,1)
									time.sleep(1)
								elif data == "LED4_Y\n":
									print ("Led 4 YELLOW")
									tricolor.turnOnLed (4,0)
									time.sleep(1)
								elif data == "LED4_OFF\n":
									print ("Led 4 OFF")
									tricolor.turnOnLed (4,3)
									time.sleep(1)
								elif data == "LED5_R\n":
									print ("Led 5 RED")
									tricolor.turnOnLed (5,2)
									time.sleep(1)
								elif data == "LED5_G\n":
									print ("Led 5 GREEN")
									tricolor.turnOnLed (5,1)
									time.sleep(1)
								elif data == "LED5_Y\n":
									print ("Led 5 YELLOW")
									tricolor.turnOnLed (5,0)
									time.sleep(1)
								elif data == "LED5_OFF\n":
									print ("Led 5 OFF")
									tricolor.turnOnLed (5,3)
									time.sleep(1)
								elif data == "LED6_R\n":
									print ("Led 6 RED")
									tricolor.turnOnLed (6,2)
									time.sleep(1)
								elif data == "LED6_G\n":
									print ("Led 6 GREEN")
									tricolor.turnOnLed (6,1)
									time.sleep(1)
								elif data == "LED6_Y\n":
									print ("Led 6 YELLOW")
									tricolor.turnOnLed (6,0)
									time.sleep(1)
								elif data == "LED6_OFF\n":
									print ("Led 6 OFF")
									tricolor.turnOnLed (6,3)
									time.sleep(1)
								elif data == "LED7_R\n":
									print ("Led 7 RED")
									tricolor.turnOnLed (7,2)
									time.sleep(1)
								elif data == "LED7_G\n":
									print ("Led 7 GREEN")
									tricolor.turnOnLed (7,1)
									time.sleep(1)
								elif data == "LED7_Y\n":
									print ("Led 7 YELLOW")
									tricolor.turnOnLed (7,0)
									time.sleep(1)
								elif data == "LED7_OFF\n":
									print ("Led 7 OFF")
									tricolor.turnOnLed (7,3)
									time.sleep(1)
								elif data == "LED8_R\n":
									print ("Led 8 RED")
									tricolor.turnOnLed (8,2)
									time.sleep(1)
								elif data == "LED8_G\n":
									print ("Led 8 GREEN")
									tricolor.turnOnLed (8,1)
									time.sleep(1)
								elif data == "LED8_Y\n":
									print ("Led 8 YELLOW")
									tricolor.turnOnLed (8,0)
									time.sleep(1)
								elif data == "LED8_OFF\n":
									print ("Led 8 OFF")
									tricolor.turnOnLed (8,3)
									time.sleep(1)
								elif data == "GET_CHANNEL\n":
									try:
										#if (connected_multiplexer):
										msg = 0
										multiplexerReader = wear_multiplexer_reader.WearMultiplexerReader()
										msg = str(multiplexerReader.getChannel(i2cBus))
										print "MULTIPLEXER READER - Current channel selected ", msg
										time.sleep(1)		
										#else:
										#	msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"
									except Exception as e: 
										msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"
								elif data == "GET_TEMPERATURE\n":
									try:
										msg = 0
										multiplexerReader = wear_multiplexer_reader.WearMultiplexerReader()
										msg = str(multiplexerReader.getChannel(i2cBus))
										print "MULTIPLEXER READER - Current channel selected ", msg
										time.sleep(1)		
										try:
											temperatureSensor = wear_sensor_heat.WearSensorHeat(i2cBus)
											read_val = temperatureSensor.setPrecision(4)
											msg = str(temperatureSensor.getTemperature())		
											print "HEAT SENSOR - Temperature ", msg, " C"													
										except Exception as e: 
											msg = "ERROR: HEAT SENSOR BOARD NOT CONNECTED"
									except Exception as e: 
										msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"			
								elif data == "GET_LUX\n":
									try:
										msg = 0
										multiplexerReader = wear_multiplexer_reader.WearMultiplexerReader()
										msg = str(multiplexerReader.getChannel(i2cBus))
										print "MULTIPLEXER READER - Current channel selected ", msg
										time.sleep(1)		
										try:
											#if (connected_sensor_light):
											lightSensor = wear_sensor_light.WearSensorLight(i2cBus)
											time.sleep(1)	
											msg = str(lightSensor.getLux())		
											print "LIGHT SENSOR - Light ", msg, " Lux"													
										except Exception as e: 
											msg = "ERROR: LIGHT SENSOR BOARD NOT CONNECTED"
									except Exception as e: 
										msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"		
								elif data == "GET_MOTION\n":
									try:
										msg = 0
										multiplexerReader = wear_multiplexer_reader.WearMultiplexerReader()
										msg = str(multiplexerReader.getChannel(i2cBus))
										print "MULTIPLEXER READER - Current channel selected ", msg
										time.sleep(1)		
										try:
											motionSensor = wear_sensor_motion.WearSensorMotion(i2cBus)
											time.sleep(1)
											x = motionSensor.getXAxis()		
											y = motionSensor.getYAxis()		
											z = motionSensor.getZAxis()	
											msg = str(x) + "X&" + str(y) + "Y&" + str(z) + "Z"		
											print "MOTION SENSOR - values ", msg												
										except Exception as e: 
											msg = "ERROR: MOTION SENSOR BOARD NOT CONNECTED"
									except Exception as e: 
										msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"												
								elif data == "BOT_STOP\n":
									try:
										print ("Robot - Stop")
										bot.stopBot()
									except Exception as e:
										msg = "ERROR: BOT BOARD NOT CONNECTED"										
								elif data == "BOT_FORWARD\n":
									try:
										print ("Robot - Move forward")
										bot.stopBot()
										bot.moveForward()						
									except Exception as e:
										msg = "ERROR: BOT BOARD NOT CONNECTED"																				
								elif data == "BOT_BACKWARD\n":
									try:
										print ("Robot - Move backward")
										bot.stopBot()
										bot.moveBackwards()	
									except Exception as e:
										msg = "ERROR: BOT BOARD NOT CONNECTED"																				
								else:
									msg = "ERROR: WRONG CODE"
								print msg		
								"""			
								elif subdata == "SET_CHANNEL":  #format to set an specific channel on the multiplexer board SETCHANNEL%1
									if (connected_multiplexer):
										try:
											subvalue = float (data[subdata_pos+1:])
											#print "subvalue =", subvalue
											
											if subvalue < 1 or subvalue > 16:
												msg = "ERROR: VALUE OUT OF RANGE"			
												print ("Multiplexer board SET CHANNEL - ", msg)			
											else:
												result = multiplexer.setChannel(subvalue)
												print "MULTIPLEXER board - Enabling channel ",subvalue," in the board... ", result
												time.sleep(1) 										
										except ValueError:
											msg = "ERROR: INVALID CHANNEL VALUE"
									else:
										msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"
								"""		
								"""
								elif data == "7DISPLAY_OFF\n":
									print ("7 segment display - Clean display")
									display.clean()
								elif subdata1 == "7DISPLAY_ON":  #format for values 7DISPLAY_ON&1234
									try:
										subvalue1 = data[subdata1_pos+1:]
									except ValueError:
										msg = "ERROR: INVALID VALUE"
										subvalue1 = 0
									#print "subvalue1=", subvalue1
									if subvalue1 == "":
										msg = "ERROR: NO NUMBER TO DISPLAY"			
										print ("7 segment display - ", msg)			
									else:
										display.clean()
										display.showValue (n)
										print ("7 segment display - ", subvalue1)
								else:
									msg = "ERROR: WRONG CODE"
									print msg
								"""
								
								# Add data to message queue
								message_queues[s].put(msg + "\n")
								
								# Add output channel for response
								if s not in outputs:
									outputs.append(s)
									
							else:
								try:
									# Interpret empty result as closed connection
									print 'closing', client_address, 'after reading no data'
									# Stop listening for input on the connection
									if s in outputs:
										outputs.remove(s)
									inputs.remove(s)
									s.close()						

									# Remove message queue
									del message_queues[s]	
								except:
									print 'ERROR: Empty result interpreted as closed connection'
					
					# Handle outputs
					for s in writable:
						try:
							next_msg = message_queues[s].get_nowait()
						except Queue.Empty:
							# No messages waiting so stop checking for writability.
							print 'output queue for', s.getpeername(), 'is empty'
							outputs.remove(s)
						else:
							print 'sending "%s" to %s' % (next_msg, s.getpeername())
							s.send(next_msg)		

					# Handle "exceptional conditions"
					for s in exceptional:
						print 'handling exceptional condition for', s.getpeername()
						# Stop listening for input on the connection
						inputs.remove(s)
						if s in outputs:
							outputs.remove(s)
						s.close()

						# Remove message queue
						del message_queues[s]						
			
			except socket.error as msg:
				print "ERROR: Socket error! %s" % msg
				connected = False
				#break	

			except KeyboardInterrupt:
				print "Socket stopped..."
				if connected: connection.close()
				server.close()
				# Notify threads it's time to exit
				exitFlag = 1
				exit(0)

			except:
				print "ERROR: Unexpected error - while inputs:", sys.exc_info()[0]
				exitFlag = 1			
				
	except KeyboardInterrupt:
		print "Socket stopped..."
		if connected: connection.close()
		server.close()
		# Notify threads it's time to exit
		exitFlag = 1
		exit(0)

	except socket.error as msg:
		server = None
		print "ERROR: Socket error! %s" % msg	
		#server.close()
		exitFlag = 1
		exit(0)		

	except Exception as e: 
		print "ERROR: Unexpected error:", e #sys.exc_info()[0]
		exitFlag = 1	