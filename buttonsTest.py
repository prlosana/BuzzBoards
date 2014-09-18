import smbus
import time
import datetime

# Access the i2c bus 
bus = smbus.SMBus(1)

# Adress of the device (i2cdetect -y 0)
addr_l = 0x23
addr_b = 0x22
all_green = 0x5555
all_red = 0xAAAA
all_yellow = 0x0000
all_off = 0xFFFF
read_val = 0x00
val = 0x00
b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = False

# Clean leds
bus.write_byte_data(addr_l,all_off, all_off)

# Read values
while 1:
	# Default value 255 (0xFF)
	val = bus.read_byte(addr_b)	
	# print "value = ", val
	
	if val==254: # 0xFE
		b1 = True
		b2 = b3 = b4 = b5 = b6 = b7 = b8 = False
		read_val = val
	elif val==253: # 0xFD
		b2 = True
		b1 = b3 = b4 = b5 = b6 = b7 = b8 = False
		read_val = val
	elif val==251: # 0xFB
		b3 = True
		b2 = b1 = b4 = b5 = b6 = b7 = b8 = False
		read_val = val
	elif val==247: # 0xF7
		b4 = True
		b2 = b3 = b1 = b5 = b6 = b7 = b8 = False
		read_val = val
	elif val==239: # 0xEF
		b5 = True
		b2 = b3 = b4 = b1 = b6 = b7 = b8 = False
		read_val = val
	elif val==223: # 0xDF
		b6 = True
		b2 = b3 = b4 = b5 = b1 = b7 = b8 = False
		read_val = val
	elif val==191: # 0xBF
		b7 = True
		b2 = b3 = b4 = b5 = b6 = b1 = b8 = False
		read_val = val
	elif val==127: # 0x7F
		b8 = True
		b2 = b3 = b4 = b5 = b6 = b7 = b1 = False
		read_val = val
	#elif bus.read_byte(addr_b)==0xFF:
		#bus.write_byte_data(addr_l,all_off, all_off)

	if b1:
		bus.write_byte_data(addr_l,all_red, all_off)
	elif b2:
		bus.write_byte_data(addr_l,all_green, all_off)
	elif b3:
		bus.write_byte_data(addr_l,all_yellow, all_off)
	elif b4:
		bus.write_byte_data(addr_l,all_yellow, all_off)
	elif b5:
		bus.write_byte_data(addr_l,all_off, all_yellow)
	elif b6:
		bus.write_byte_data(addr_l,all_off, all_green)
	elif b7:
		bus.write_byte_data(addr_l,all_off, all_green)
	elif b8:
		bus.write_byte_data(addr_l,all_off, all_red)
	else:
		bus.write_byte_data(addr_l,all_off, all_off)

	print "B1 =", b1, ", B2 =", b2, ", B3 =", b3, ", B4=", b4, ", B5=", b5, ", B6=", b6, ", B7=", b7, ", B8=", b8 , ", Value =", read_val
