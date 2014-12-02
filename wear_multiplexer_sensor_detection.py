import wear_multiplexer
import wear_sensor_light
import wear_sensor_heat
import wear_sensor_motion

#Global variables
#-------------------------------------------------------------------------------
bus = 1			#This depends on the model of the Raspberry Pi	
read_val = 0
connected_multiplexer = False
connected_sensor_light = False
connected_sensor_temp = False
connected_sensor_motion = False

if __name__ == "__main__":
	#Main program
	#-------------------------------------------------------------------------------
	aux = True
	try:
		while aux:
			#Enable multiplexer
			try:
				while (not connected_multiplexer):
					result = ""
					multiplexer = wear_multiplexer.WearMultiplexer(bus)
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
								
								if (not connected_sensor_temp):
									try:
										#Start temperature sensor
										temperatureSensor = wear_sensor_heat.WearSensorHeat(bus)

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
										lightSensor = wear_sensor_light.WearSensorLight(bus)
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
								print "ERROR: MULTIPLEXER - ", e		
						else:
							break

				#Start reading sensors
				if (connected_sensor_temp):
					try:
						result = temperatureSensor.getTemperature()		
						print "HEAT SENSOR - Temperature ", result, " C"
					except Exception as e: 
						print "ERROR: HEAT SENSOR - ", e		
						connected_sensor_temp = False
				
				if (connected_sensor_light):
					try: 
						result = lightSensor.getLux()
						print "LIGHT SENSOR - Lux ", result						
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
				print "ERROR: MULTIPLEXER - ", e		
				connected_multiplexer = False

	except KeyboardInterrupt:
		print "Service detection stopped..."
		aux = False