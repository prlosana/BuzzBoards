import time
import buzzbox
import tricolourleds8
import buttons8
import wear_multiplexer
import wear_multiplexer_reader
import wear_sensor_heat
import wear_sensor_light
import wear_sensor_motion

#Global variables
#-------------------------------------------------------------------------------
i2cBus = 1	#This depends on the model of the Raspberry Pi	
connected_multiplexer = False	 
connected_sensorTemperature = False
connected_sensorLight = False
connected_sensorMotion = False

if __name__ == "__main__":
	print ("----------------------------------------------------")
	print ("running - BUZZBOX test")
	print ("----------------------------------------------------")

	#Creates box instance
	try: 
		box = buzzbox.BuzzBox(i2cBus)
		box.clean()
	except Exception as e: 
		print "ERROR: BUZZBOX Unexpected error:", e
		
	#Creates tricolour leds instance
	try: 
		# Colour code: 0=yellow, 1=green, 2=red, 3=off
		tricolor = tricolourleds8.TricolourLeds8(i2cBus)
		tricolor.clean()		
	except Exception as e: 
		print "ERROR: TRICOLOUR LEDS Unexpected error:", e

	#Creates multiplexer board instance
	try:
		multiplexer = wear_multiplexer.WearMultiplexer(i2cBus)
		
		#Unless using the discovery service, we need to specify in which jack sockets
		# are the sensors connected - CHECK THE PORT USED AND CHANGE IT IN THE VAR channel 
		channel = 0
		result = multiplexer.setChannel(channel)
		print "MULTIPLEXER - Enabling channel ",channel," in the board... ", result
		
		channel = multiplexer.getChannel()
		print "MULTIPLEXER - Current channel selected ",channel
		connected_multiplexer = True	
			
	except Exception as e: 
		print "ERROR: MULTIPLEXER BOARD Unexpected error:", e
	
	#Creates temperature sensor board instance
	try:
		if (connected_multiplexer):
			temperatureSensor = wear_sensor_heat.WearSensorHeat(i2cBus)
			connected_sensorTemperature = True		
	except Exception as e: 
		print "ERROR: TEMPERATURE SENSOR BOARD Unexpected error:", e

	#Creates light sensor board instance
	try:
		if (connected_multiplexer):
			lightSensor = wear_sensor_light.WearSensorLight(i2cBus)
			connected_sensorLight = True		
	except Exception as e: 
		print "ERROR: LIGHT SENSOR BOARD Unexpected error:", e

	#Creates motion sensor board instance
	try:
		if (connected_multiplexer):
			motionSensor = wear_sensor_motion.WearSensorMotion(i2cBus)
			connected_sensorMotion = True		
	except Exception as e: 
		print "ERROR: MOTION SENSOR BOARD Unexpected error:", e

	#Start test
	try:
		#Lighting set 1 ON
		box.setLighting1 (True, 0, False)
		print "Lighting set 1 STATUS", box.getLighting1()
		time.sleep(5) 			#5 seconds wait

		#Lighting set 1 BLINK
		box.setLighting1 (True, 0, True)
		print "Lighting set 1 STATUS", box.getLighting1()
		time.sleep(5) 			

		#Lighting set 1 DIMMABLE 50%
		box.setLighting1 (True, 0.5, False)
		print "Lighting set 1 STATUS", box.getLighting1()
		time.sleep(5) 			

		#Lighting set 2 ON
		box.setLighting2 (True, 0, False)
		print "Lighting set 2 STATUS", box.getLighting2()
		time.sleep(5)

		#Lighting set 2 BLINK
		box.setLighting2 (True, 0, True)
		print "Lighting set 2 STATUS", box.getLighting2()
		time.sleep(5) 			

		#Lighting set 2 DIMMABLE 5%
		box.setLighting2 (True, 0.05, False)
		print "Lighting set 2 STATUS", box.getLighting2()
		time.sleep(5) 			

		#Fan ON
		box.setFan (True)
		print "Fan STATUS", box.getFan()
		time.sleep(2)

		#Heater ON
		box.setHeater (True)
		print "Heater STATUS", box.getHeater()
		time.sleep(2)

		#LED's changing colours
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
	
		#Clear all LED's
		tricolor.clean()
	
		
		#Temperature sensor
		if (connected_sensorTemperature):
			read_val = temperatureSensor.setPrecision(4)
			print "HEAT SENSOR - Set precision, no. of decimals = 4 Result - ", read_val
		
			result = temperatureSensor.getTemperature()		
			print "HEAT SENSOR - Temperature ", result, " C"

		#Light sensor
		if (connected_sensorLight):
			result = lightSensor.getLux()
			print "LIGHT SENSOR - Lux ", result		

		#Motion sensor
		if (connected_sensorMotion):
			x = motionSensor.getXAxis()		
			y = motionSensor.getYAxis()		
			z = motionSensor.getZAxis()		
			print "MOTION SENSOR - X=", x, ", Y=", y, ", Z=", z
			tilt = motionSensor.getPosition()
			print "MOTION SENSOR - POSITION=", tilt
			tilt = motionSensor.getOrientation()
			print "MOTION SENSOR - ORIENTATION=", tilt						
			
		#Lighting set 1 OFF
		box.setLighting1 (False, 0, False)
		print "Lighting set 1 STATUS", box.getLighting1()

		#Lighting set 2 OFF
		box.setLighting2 (False, 0, False)
		print "Lighting set 2 STATUS", box.getLighting2()

		#Fan OFF
		box.setFan (False)
		print "Fan STATUS", box.getFan()

		#Heater OFF
		box.setHeater (False)
		print "Heater STATUS", box.getHeater()

		print ("----------------------------------------------------")
		print("finished - BUZZBOX test")
		print ("----------------------------------------------------")
	
	except Exception as e: 
		print "ERROR: ", e
