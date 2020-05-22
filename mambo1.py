from pyparrot.Minidrone import *
import socket
from time import sleep
import threading
from dance import *
import sys

mamboAddr = "D0:3A:DD:15:E6:21"	#639619 is "D0:3A:DD:15:E6:21"
								
mambo = Mambo(mamboAddr, use_wifi=False)
HOST = '127.0.0.1'
PORT = 1111

def keep_listen():
	while True:
		print('\n [Thread] Waiting for Operation')
		data.append(conn1.recv(1024).decode())
		print('current data is: '+data[-1]+'\n')
		if (data[-1] == '100'):
			m1.close()
			sys.exit(1)
			break


def Emergency_land():
	#mambo.safe_land(5)
	mambo.smart_sleep(1)
	#mambo.disconnect()


def drone_sync():
	if (data[-1]!='-15'):
		conn1.sendall('g1'.encode())
	while True:
		if (data[-1]=='g1'):
			mambo.smart_sleep(1)
			data.append('1000')
			break
		elif (data[-1]=='-15'):
			Emergency_land()
			break
		mambo.smart_sleep(0.1)




try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as m1:
		m1.bind((HOST,PORT))
		print('Waiting for Client Connection')
		m1.listen()
		conn1, addr = m1.accept()
		with conn1:
			print('Connected With Client')
			data = []
			data.append('1000')
			t = threading.Thread(target=keep_listen)
			t.start()
			print("Connecting to Mambo1")
			success = mambo.connect(num_retries=5)
			print("Connected: %s" % success)
			if (success):
				mambo.smart_sleep(1)
				mambo.ask_for_state_update()	# get the state information
				print("Waiting for Command!!")
				while True:
					if (data[-1]=='-1T'): #Takeoff
						mambo.safe_takeoff(5)
						data.append('1000')
						print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='1-1'):#Dance1
						dance_1L(mambo,conn1, data)
						data.append('1000')
						print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='2-1'):#Dance2
						dance_2L(mambo,conn1, data)
						data.append('1000')
						print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='3-1'):#Dance3
						dance_3L(mambo,conn1, data)
						data.append('1000')
						print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='-10'):#Landing
						if (mambo.sensors.flying_state != "emergency"):
							mambo.safe_land(5)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='05'or data[-1]=='451'):# Minus Pitch
						if (mambo.sensors.flying_state != "emergency"):
							mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=0, duration=0.7)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='0P'or data[-1]=='4P1'):# Plus Pitch
						if (mambo.sensors.flying_state != "emergency"):
							mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=0.7)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='0L'or data[-1]=='4L1'):# Minus Roll
						if (mambo.sensors.flying_state != "emergency"):
							mambo.fly_direct(roll=-30, pitch=0, yaw=0, vertical_movement=0, duration=0.7)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='0R'or data[-1]=='4R1'):# Plus Roll
						if (mambo.sensors.flying_state != "emergency"):
							mambo.fly_direct(roll=30, pitch=-0, yaw=0, vertical_movement=0, duration=0.7)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='01'or data[-1]=='411'):# left Turn
						if (mambo.sensors.flying_state != "emergency"):
							mambo.turn_degrees(90)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='02'or data[-1]=='421'):# Right turn
						if (mambo.sensors.flying_state != "emergency"):
							mambo.turn_degrees(-90)
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='03'or data[-1]=='431'):# Flip
						if (mambo.sensors.flying_state != "emergency"):
							mambo.flip(direction="back")
							mambo.smart_sleep(1)
							data.append('1000')
							print("Waiting for command Current Data : "+data[-1])
					elif (data[-1]=='-15'):# Emergency Landing
						mambo.smart_sleep(1)
						data.append('1000')
					elif (data[-1]=='100'):#disconnect()
						m1.close()
						print("shutdown")
						break
					else:
						mambo.smart_sleep(0.1)	
			else:
				print('Mambo Connection Fail. Reboot Mambo and Try Again')
				m1.close()

			print('Program Terminate')

except KeyboardInterrupt:
	m1.close()
	print("Closing...")
