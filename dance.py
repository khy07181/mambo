'''
Mambo 1,3
'''

def Emergency_land(mambo):
	mambo.safe_land(5)
	mambo.smart_sleep(1)
	mambo.disconnect()


def drone_sync(mambo, conn1, data):
	if (data[-1]!='-15'):
		conn1.sendall('g1'.encode())
	while True:
		if (data[-1]=='g1'):
			mambo.smart_sleep(1)
			data.append('1000')
			break
		elif (data[-1]=='-15'):
			Emergency_land(mambo)
			break
		mambo.smart_sleep(0.1)

def dance_1L(mambo, conn1, data):
	if (mambo.sensors.flying_state != "emergency"):
		mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=0.5)
		mambo.smart_sleep(1)
		mambo.turn_degrees(90)
		mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=1.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-40, duration=1.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)

def dance_2L(mambo,conn1, data):
	if (mambo.sensors.flying_state != "emergency"):
		mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=1)
		mambo.smart_sleep(1)
		mambo.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=1)
		mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.8)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=1.7)
			mambo.smart_sleep(1.5)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.flip(direction="back")
			mambo.smart_sleep(1.5)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=-40, yaw=0, vertical_movement=0, duration=1)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=-50, pitch=0, yaw=0, vertical_movement=0, duration=0.7)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=40, yaw=0, vertical_movement=0, duration=1)
			mambo.smart_sleep(1)
			


def dance_3L(mambo,conn1, data):
	if (mambo.sensors.flying_state != "emergency"):
		mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=1)
		mambo.turn_degrees(-90)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=45, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(2)
			mambo.flip(direction="front")
			mambo.smart_sleep(2)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(-90)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=45, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(2)
			mambo.flip(direction="back")
			mambo.smart_sleep(2)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(-90)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=45, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(2)
			mambo.flip(direction="back")
			mambo.smart_sleep(2)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(-90)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=0, yaw=100, vertical_movement=20, duration=3)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=0, yaw=100, vertical_movement=-20, duration=3)
			mambo.smart_sleep(1)
			mambo.turn_degrees(-90)



'''

mambo 2,4
'''

def dance_1R(mambo,conn1, data):
	if (mambo.sensors.flying_state != "emergency"):
		mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=0.5)
		mambo.smart_sleep(1)
		mambo.turn_degrees(90)
		mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-40, duration=1.5)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=1.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-40, duration=0.5)
			mambo.smart_sleep(1)

def dance_2R(mambo,conn1, data):
	if (mambo.sensors.flying_state != "emergency"):
		mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=1)
		mambo.smart_sleep(1)
		mambo.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=1)
		mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=-50, pitch=0, yaw=0, vertical_movement=0, duration=0.8)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=40, yaw=0, vertical_movement=0, duration=1.7)
			mambo.smart_sleep(1.5)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.flip(direction="back")
			mambo.smart_sleep(1.5)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=40, yaw=0, vertical_movement=0, duration=1)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.7)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=-0, duration=1)
			mambo.smart_sleep(1)
			



def dance_3R(mambo,conn1, data):
	if (mambo.sensors.flying_state != "emergency"):
		mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=40, duration=1)
		mambo.turn_degrees(90)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=45, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(2)
			mambo.flip(direction="front")
			mambo.smart_sleep(2)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=45, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(2)
			mambo.flip(direction="back")
			mambo.smart_sleep(2)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=45, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(2)
			mambo.flip(direction="back")
			mambo.smart_sleep(2)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.turn_degrees(90)
			mambo.smart_sleep(1)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=0.5)
			mambo.smart_sleep(1)
			mambo.fly_direct(roll=0, pitch=0, yaw=100, vertical_movement=20, duration=3)
		drone_sync(mambo, conn1, data)#Sync here
		if (data[-1]!='-15'):
			mambo.fly_direct(roll=0, pitch=0, yaw=100, vertical_movement=-20, duration=3)
			mambo.smart_sleep(1)
			mambo.turn_degrees(-90)
