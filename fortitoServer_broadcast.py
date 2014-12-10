import time
import pygame
import buzzbox
import tricolourleds8
import buttons8
import wear_multiplexer
import wear_sensor_heat
import wear_sensor_light
import wear_sensor_motion

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, task

i2cBus = 1	#This depends on the model of the Raspberry Pi
box = None
tricolor = None
buttons = None
multiplexer = None
temperatureSensor = None
lightSensor = None
motionSensor = None

connected_multiplexer = False
connected_sensor_light = False
connected_sensor_temp = False
connected_sensor_motion = False
current_channel = 0

#Creates box instance
try: 
	box = buzzbox.BuzzBox(i2cBus)
	box.clean()
except Exception as e: 
	print ("ERROR: BUZZBOX Unexpected error:", e) #sys.exc_info()[0]
	#exitFlag = 1

#Creates tricolour leds instance
try: 
	# Colour code: 0=yellow, 1=green, 2=red, 3=off
	tricolor = tricolourleds8.TricolourLeds8(i2cBus)
	tricolor.clean()
except Exception as e: 
	print ("ERROR: TRICOLOUR LEDS Unexpected error:", e)
	#exitFlag = 1

#Creates buttons instance
try: 
	buttons = buttons8.Buttons8(i2cBus)
	buttons.clean()
except Exception as e: 
	print ("ERROR: BUTTONS Unexpected error:", e)
	#exitFlag = 1

#Creates multiplexer instance
try:
	multiplexer = wear_multiplexer.WearMultiplexer(i2cBus)
	connected_multiplexer = True
except Expection as e:
	connected_multiplexer = False
	print ("ERROR: Multiplexer Unexpected error:", e)
	#exitFlag = 1
	
class Fortito(Protocol):

	def __init__(self, factory):
		self.factory = factory
		#Starts service for buttons
		self.buttons_checker = task.LoopingCall(self.get_BUTTONS_STATUS)
		self.buttons_checker.start(1, True)
		#Starts service for sensors
		self.sensors_checker = task.LoopingCall(self.sensorDiscoveryService)
		self.sensors_checker.start(1, True)

	def connectionMade(self):
		self.factory.clients.append(self)
		print ("Client connected.")#, self.factory.clients)

	def connectionLost(self, reason):
		self.factory.clients.remove(self)

	def dataReceived(self, data):
		print ("Data received: ", data)
		self.get_BUZZBOX_STATUS(data)

	def handle_MESSAGE(self, message):
		for client in self.factory.clients:
			client.transport.write(message)

	def get_BUTTONS_STATUS(self):
		global buttons
		
		#print ("get_BUTTONS_STATUS running......") 
		result = buttons.readValue()
		if result <> "":
			print (str(result), " pressed..............")
			self.handle_MESSAGE(str(result) + "\n")
			result = ""	

	def get_BUZZBOX_STATUS(self, data):
		global i2cBus
		global box
		global tricolor
		global buttons
		global multiplexer
		global temperatureSensor
		global lightSensor
		global motionSensor
		global connected_multiplexer
		global connected_sensor_light
		global connected_sensor_temp
		global connected_sensor_motion
		global current_channel

		#Evaluates data
		data = data.upper()
		msg = "OK"
		
		subdata_pos = data.find("%")
		subdata = data[0:subdata_pos]
		subvalue = 0
		#print "character % found at ", subdata_pos, " command ", subdata

		subdata1_pos = data.find("&")
		subdata1 = data[0:subdata1_pos]
		subvalue1 = 0
		if data == "HELLO\n":
			msg = "Greetings!"
			print ("Greetings!")
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
		elif data == "LIGHT1_BLINK\n":
			print ("Lighting set 1 BLINK")
			box.setLighting1 (True, 0, True)
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
		elif data == "GET_LIGHT1\n":
			msg = box.getLighting1()
			print ("Lighting set 1  - Get status ",msg)
		elif data == "LIGHT2_ON\n":
			print ("Lighting set 2 ON")
			box.setLighting2 (True, 0, False)
		elif data == "LIGHT2_BLINK\n":
			print ("Lighting set 2 BLINK")
			box.setLighting2 (True, 0, True)
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
		elif data == "GET_LIGHT2\n":
			msg = box.getLighting2()
			print ("Lighting set 2  - Get status ",msg)
		elif data == "FAN_ON\n":
			print ("Fan ON")
			box.setFan (True)
		elif data == "HEATER_ON\n":
			print ("Heater ON")
			box.setHeater (True)
		elif data == "LIGHT1_OFF\n":
			print ("Lighting set 1 OFF")
			box.setLighting1 (False, 0, False)
		elif data == "LIGHT2_OFF\n":
			print ("Lighting set 2 OFF")
			box.setLighting2 (False, 0, False)
		elif data == "FAN_OFF\n":
			print ("Fan OFF")
			box.setFan (False)
		elif data == "HEATER_OFF\n":
			print ("Heater OFF")
			box.setHeater (False)
		elif data == "GET_FAN\n":
			msg = box.getFan()
			print ("Fan  - Get status ",msg)
		elif data == "GET_HEATER\n":
			msg = box.getHeater()
			print ("Heater  - Get status ",msg)
		elif data == "PRESS_BTN1\n":
			msg = buttons.readValueVirtualBtn("BTN1")
			print ("Virtual BTN1 - Get status ", msg)
		elif data == "PRESS_BTN2\n":
			msg = buttons.readValueVirtualBtn("BTN2")
			print ("Virtual BTN2 - Get status ", msg)
		elif data == "PRESS_BTN3\n":
			msg = buttons.readValueVirtualBtn("BTN3")
			print ("Virtual BTN3 - Get status ", msg)
		elif data == "PRESS_BTN4\n":
			msg = buttons.readValueVirtualBtn("BTN4")
			print ("Virtual BTN4 - Get status ", msg)
		elif data == "PRESS_BTN5\n":
			msg = buttons.readValueVirtualBtn("BTN5")
			print ("Virtual BTN5 - Get status ", msg)
		elif data == "PRESS_BTN6\n":
			msg = buttons.readValueVirtualBtn("BTN6")
			print ("Virtual BTN6 - Get status ", msg)
		elif data == "PRESS_BTN7\n":
			msg = buttons.readValueVirtualBtn("BTN7")
			print ("Virtual BTN7 - Get status ", msg)
		elif data == "PRESS_BTN8\n":
			msg = buttons.readValueVirtualBtn("BTN8")
			print ("Virtual BTN8 - Get status ", msg)
		elif data == "GET_LED1\n":
			msg = tricolor.getLed1()
			print ("Led 1  - Get status ",msg)
		elif data == "GET_LED2\n":
			msg = tricolor.getLed2()
			print ("Led 2  - Get status ",msg)
		elif data == "GET_LED3\n":
			msg = tricolor.getLed3()
			print ("Led 3  - Get status ",msg)
		elif data == "GET_LED4\n":
			msg = tricolor.getLed4()
			print ("Led 4  - Get status ",msg)
		elif data == "GET_LED5\n":
			msg = tricolor.getLed5()
			print ("Led 5  - Get status ",msg)
		elif data == "GET_LED6\n":
			msg = tricolor.getLed6()
			print ("Led 6  - Get status ",msg)
		elif data == "GET_LED7\n":
			msg = tricolor.getLed7()
			print ("Led 7  - Get status ",msg)
		elif data == "GET_LED8\n":
			msg = tricolor.getLed8()
			print ("Led 8  - Get status ",msg)
		elif data == "LED1_R\n":
			print ("Led 1 RED")
			tricolor.turnOnLed (1,2)
		elif data == "LED1_G\n":
			print ("Led 1 GREEN")
			tricolor.turnOnLed (1,1)
		elif data == "LED1_Y\n":
			print ("Led 1 YELLOW")
			tricolor.turnOnLed (1,0)
		elif data == "LED1_OFF\n":
			print ("Led 1 OFF")
			tricolor.turnOnLed (1,3)
		elif data == "LED2_R\n":
			print ("Led 2 RED")
			tricolor.turnOnLed (2,2)
		elif data == "LED2_G\n":
			print ("Led 2 GREEN")
			tricolor.turnOnLed (2,1)
		elif data == "LED2_Y\n":
			print ("Led 2 YELLOW")
			tricolor.turnOnLed (2,0)
		elif data == "LED2_OFF\n":
			print ("Led 2 OFF")
			tricolor.turnOnLed (2,3)
		elif data == "LED3_R\n":
			print ("Led 3 RED")
			tricolor.turnOnLed (3,2)
		elif data == "LED3_G\n":
			print ("Led 3 GREEN")
			tricolor.turnOnLed (3,1)
		elif data == "LED3_Y\n":
			print ("Led 3 YELLOW")
			tricolor.turnOnLed (3,0)
		elif data == "LED3_OFF\n":
			print ("Led 3 OFF")
			tricolor.turnOnLed (3,3)
		elif data == "LED4_R\n":
			print ("Led 4 RED")
			tricolor.turnOnLed (4,2)
		elif data == "LED4_G\n":
			print ("Led 4 GREEN")
			tricolor.turnOnLed (4,1)
		elif data == "LED4_Y\n":
			print ("Led 4 YELLOW")
			tricolor.turnOnLed (4,0)
		elif data == "LED4_OFF\n":
			print ("Led 4 OFF")
			tricolor.turnOnLed (4,3)
		elif data == "LED5_R\n":
			print ("Led 5 RED")
			tricolor.turnOnLed (5,2)
		elif data == "LED5_G\n":
			print ("Led 5 GREEN")
			tricolor.turnOnLed (5,1)
		elif data == "LED5_Y\n":
			print ("Led 5 YELLOW")
			tricolor.turnOnLed (5,0)
		elif data == "LED5_OFF\n":
			print ("Led 5 OFF")
			tricolor.turnOnLed (5,3)
		elif data == "LED6_R\n":
			print ("Led 6 RED")
			tricolor.turnOnLed (6,2)
		elif data == "LED6_G\n":
			print ("Led 6 GREEN")
			tricolor.turnOnLed (6,1)
		elif data == "LED6_Y\n":
			print ("Led 6 YELLOW")
			tricolor.turnOnLed (6,0)
		elif data == "LED6_OFF\n":
			print ("Led 6 OFF")
			tricolor.turnOnLed (6,3)
		elif data == "LED7_R\n":
			print ("Led 7 RED")
			tricolor.turnOnLed (7,2)
		elif data == "LED7_G\n":
			print ("Led 7 GREEN")
			tricolor.turnOnLed (7,1)
		elif data == "LED7_Y\n":
			print ("Led 7 YELLOW")
			tricolor.turnOnLed (7,0)
		elif data == "LED7_OFF\n":
			print ("Led 7 OFF")
			tricolor.turnOnLed (7,3)
		elif data == "LED8_R\n":
			print ("Led 8 RED")
			tricolor.turnOnLed (8,2)
		elif data == "LED8_G\n":
			print ("Led 8 GREEN")
			tricolor.turnOnLed (8,1)
		elif data == "LED8_Y\n":
			print ("Led 8 YELLOW")
			tricolor.turnOnLed (8,0)
		elif data == "LED8_OFF\n":
			print ("Led 8 OFF")
			tricolor.turnOnLed (8,3)
		elif data == "GET_CHANNEL\n":
			try:
				msg = 0
				msg = str(multiplexer.getChannel(i2cBus))
				print "MULTIPLEXER - Current channel selected ", msg
			except Exception as e: 
				msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"
		elif data == "GET_TEMPERATURE\n":
			try:
				msg = 0
				msg = str(multiplexer.getChannel(i2cBus))
				#print "MULTIPLEXER - Current channel selected ", msg
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
				msg = str(multiplexer.getChannel(i2cBus))
				#print "MULTIPLEXER - Current channel selected ", msg
				try:
					lightSensor = wear_sensor_light.WearSensorLight(i2cBus)
					msg = str(lightSensor.getLux())
					print "LIGHT SENSOR - Light ", msg, " Lux"
				except Exception as e: 
					msg = "ERROR: LIGHT SENSOR BOARD NOT CONNECTED"
			except Exception as e: 
				msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"
		elif data == "GET_MOTION\n":
			try:
				msg = 0
				msg = str(multiplexer.getChannel(i2cBus))
				#print "MULTIPLEXER - Current channel selected ", msg
				try:
					motionSensor = wear_sensor_motion.WearSensorMotion(i2cBus)
					x = motionSensor.getXAxis()
					y = motionSensor.getYAxis()
					z = motionSensor.getZAxis()
					msg = str(x) + "X&" + str(y) + "Y&" + str(z) + "Z"
					print "MOTION SENSOR - values ", msg
				except Exception as e: 
					msg = "ERROR: MOTION SENSOR BOARD NOT CONNECTED"
			except Exception as e: 
				msg = "ERROR: MULTIPLEXER BOARD NOT CONNECTED"
		else:
			msg = "ERROR: WRONG CODE"
		
		print ("Result: ", msg + "\n")
		self.handle_MESSAGE(msg + "\n")

	def sensorDiscoveryService(self):
		global i2cBus
		global multiplexer
		global temperatureSensor
		global lightSensor
		global motionSensor
		global connected_multiplexer
		global connected_sensor_light
		global connected_sensor_temp
		global connected_sensor_motion
		global current_channel
	
		#print ("sensorDiscoveryService running......") 
		if (connected_sensor_temp or connected_sensor_light or connected_sensor_motion):
			pass
		else:
			print ("sensorDiscoveryService running......") 
			for channel in range(1,17):
				try:
					result = multiplexer.setChannel(channel)
					print ("MULTIPLEXER - Enabling channel ",channel," in the board... ", result)
					
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

		#Start reading sensors
		if (connected_sensor_temp):
			try:
				result = temperatureSensor.getTemperature()
				#print ("HEAT SENSOR - Temperature ", result, " C")
			except Exception as e: 
				#print ("ERROR: HEAT SENSOR - ", e)
				connected_sensor_temp = False

		if (connected_sensor_light):
			try: 
				result = lightSensor.getLux()
				#print ("LIGHT SENSOR - Lux ", result)
			except Exception as e: 	
				#print ("ERROR: LIGHT SENSOR - ", e)
				connected_sensor_light = False

		if (connected_sensor_motion):
			try: 
				x = motionSensor.getXAxis()
				y = motionSensor.getYAxis()
				z = motionSensor.getZAxis()
				#print ("MOTION SENSOR - X=", x, ", Y=", y, ", Z=", z)
			except Exception as e: 	
				#print ("ERROR: MOTION SENSOR - ", e)
				connected_sensor_motion = False
			
class FortitoFactory(Factory):
	def __init__(self):
		self.clients = []

	def buildProtocol(self, addr):
		return Fortito(self)


reactor.listenTCP(50000, FortitoFactory())
print ("Fortito server started.")
reactor.run()