import socket
import time
import threading
import pygame
import traceback
import cv2
import numpy as np
import math
import sys


#--------------------TCP Setting-----------------------------------------------
PORT1 = 1111
PORT2 = 2222
PORT3 = 3333
PORT4 = 4444
#---------------1---------------------------------------------------------------

#----------------------Video Setting ------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
cap.set(cv2.CAP_PROP_CONTRAST, 50)

count_frame =[]

current_drone=[1,2,3,4]
drone_select = 4

cmd1=[]
cmd2=[]

#------------------------------------------------------------------------------

#----------------------pygame music setting------------------------------------
music_file = '/home/juno/Drones/final/music1.mp3'
freq = 44100    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
bitsize = -16   # signed 16 bit. support 8,-8,16,-16
channels = 1    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)

#------------------------------------------------------------------------------

def keep_listen1():#listening port for mambo1
	while True:
		receive1.append(m1.recv(1024).decode())
		print('[Thread1] Signal 1 Receiived')

def keep_listen2():#listening port for mambo2
	while True:
		receive2.append(m2.recv(1024).decode())
		print('[Thread2] Signal 2 Receiived')

def keep_listen3():#listening port for mambo1
	while True:
		receive3.append(m3.recv(1024).decode())
		print('[Thread3] Signal 3 Receiived')

def keep_listen4():#listening port for mambo2
	while True:
		receive4.append(m4.recv(1024).decode())
		print('[Thread4] Signal 4 Receiived')

def keep_send():#sending Port for both Drone
	global drone_select
	while True:
		print('[Take-off:0] [Dance:1,2,3] [Landing:4] [Pitch:-5,+6] [Roll:<7,8>] [Emergency:e] [ShutDown:10]')
		print('Current drone is : '+str(current_drone[abs(drone_select)%4]))
		data = input()
		if(data == 'L-1'):
			drone_select=drone_select-1
		elif(data == 'R-1'):
			drone_select=drone_select+1
		if(data[0] == '4'):
			data=data+str(current_drone[abs(drone_select)%4])
		dance.append(data)
		m1.sendall(dance[-1].encode()) #send to 1111
		m2.sendall(dance[-1].encode()) #send to 2222
		m3.sendall(dance[-1].encode()) #send to 3333
		m4.sendall(dance[-1].encode()) #send to 4444
		time.sleep(1)
		#if(dance[-1]=='e'):
		#	pygame.mixer.music.stop()
		dance.append('1000')

def drone_music():#drone music setting
	while True:
		if (dance[-1]=='01' or dance[-1]=='02' or dance[-1]=='03'):
			pygame.mixer.init(freq, bitsize, channels, buffer)
			pygame.mixer.music.load(music_file)
			pygame.mixer.music.play()
			clock = pygame.time.Clock()
			while pygame.mixer.music.get_busy():
				clock.tick(10)
			pygame.mixer.quit()

def drone_sync():
	while True:
		if (dance[-1] =='-15'):
			print('[Emergency Going back to Main Loop]\n')
			#m1.sendall(dance[-1].encode()) #
			#m2.sendall(dance[-1].encode()) #
			break
		elif (receive1[-1]=='g1' and receive2[-1]=='g1' and receive3[-1]=='g1' and receive4[-1]=='g1' and dance[-1] !='-15'):
			print('Signal Recieved')
			m1.sendall('g1'.encode()) #send to 1111
			m2.sendall('g1'.encode()) #send to 2222
			m3.sendall('g1'.encode()) #send to 1111
			m4.sendall('g1'.encode()) #send to 2222
			receive1.append('0')
			receive2.append('0')
			receive3.append('0')
			receive4.append('0')
			break
		

def frame_count(motion_number):
	global cmd1
	global cmd2
	
	count_frame.append(motion_number)
	if (count_frame.count(motion_number)==100):
		if(motion_number == 'L-1'):
			drone_select=drone_select-1
		elif(motion_number == 'R-1'):
			drone_select=drone_select+1
		if(motion_number[0] == '4'):
			motion_number=motion_number+str(current_drone[abs(drone_select)%4])
		dance.append(motion_number)
		m1.sendall(dance[-1].encode()) #send to 1111
		m2.sendall(dance[-1].encode()) #send to 2222
		m3.sendall(dance[-1].encode()) #send to 3333
		m4.sendall(dance[-1].encode()) #send to 4444
		count_frame.clear()
		count_frame.append('0')
		cmd1.clear()
		cmd2.clear()

def capture(frame, kernel, startX, startY, endX, endY, number):
	cmd = '-1'
	drawY = 50
	non = True
	if(number == 1):
		drawY = 50
	elif(number == 2):
		drawY = 450 
		#define region of interest
	roi=frame[startX:startY, endX:endY]
	cv2.rectangle(frame,(endX,startX),(endY,startY),(0,255,0),0)    
	hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # define range of skin color in HSV
	lower_skin = np.array([0,20,70], dtype=np.uint8)
	upper_skin = np.array([20,255,255], dtype=np.uint8)
    #extract skin colur imagw  
	mask = cv2.inRange(hsv, lower_skin, upper_skin)
    #extrapolate the hand to fill dark spots within
	mask = cv2.dilate(mask,kernel,iterations = 4)
    #blur the image
	mask = cv2.GaussianBlur(mask,(5,5),100) 
    #find contours
	contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #find contour of max area(hand)
	try:	
		cnt = max(contours, key = lambda x: cv2.contourArea(x))
	except ValueError:
		non = False

	if(non):
	    #approx the contour a little
		epsilon = 0.0005*cv2.arcLength(cnt,True)
		approx= cv2.approxPolyDP(cnt,epsilon,True)
	    #make convex hull around hand
		hull = cv2.convexHull(cnt)
	    #define area of hull and area of hand
		areahull = cv2.contourArea(hull)
		areacnt = cv2.contourArea(cnt)
	    #find the percentage of area not covered by hand in convex hull
		arearatio=((areahull-areacnt)/areacnt)*100
	    #find the defects in convex hull with respect to hand
		hull = cv2.convexHull(approx, returnPoints=False)
		defects = cv2.convexityDefects(approx, hull)
	    # l = no. of defects
		l=0
	    #code for finding no. of defects due to fingers
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(approx[s][0])
			end = tuple(approx[e][0])
			far = tuple(approx[f][0])
			pt= (100,180)
		    # find length of all sides of triangle
			a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
			b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
			c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
			s = (a+b+c)/2
			ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
		    #distance between point and convex hull
			d=(2*ar)/a
		    # apply cosine rule here
			angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
		    # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
			if angle <= 90 and d>30:
				l += 1
				cv2.circle(roi, far, 3, [255,0,0], -1)
		    #draw lines around hand
			cv2.line(roi,start, end, [0,255,0], 2)
			handangle = cv2.fitEllipse(cnt)    
			#print(handangle)
		l+=1
		#print corresponding gestures which are in their ranges
		font = cv2.FONT_HERSHEY_SIMPLEX
		if l==1:
			if areacnt<2000:
				cv2.putText(frame,'Put hand',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			else:
				if (arearatio<12): 														# Safe-Land "0"
					cv2.putText(frame,'Safe-Land',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
					cmd='0'
				elif (l==1 and (160<handangle[2]<180 or 0<handangle[2]<20)):			# "1"
					cv2.putText(frame,'1',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
					cmd='1'
				elif (l==1 and (90<handangle[2]<160)):									# Go Left "L"
					cv2.putText(frame,'L',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
					cmd='L'
				elif (l==1 and (25<handangle[2]<60)): 									# Take-Off "T"
					cv2.putText(frame,'Take-Off',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
					cmd='T'
		elif (l==2 and (155<handangle[2]<180 or 0<handangle[2]<8)): 					# "2"
			cv2.putText(frame,'2',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			cmd='2'
		elif (l==2 and (8<handangle[2]<90)):											# Go Right "R"
			cv2.putText(frame,'Go Right',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			cmd='R'
		elif l==3:																		# "3"
			cv2.putText(frame,'3',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			cmd='3'
		elif (l==4):																	# "4"
			cv2.putText(frame,'4',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			cmd='4'
		elif (l==5 and (150<handangle[2]<180 or 0<handangle[2]<30)):					# "5"
			cv2.putText(frame,'Minus Pitch and E',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			cmd='5'
		elif (l==5 and (50<handangle[2]<110)):											# Plus Pitch "P"
			cv2.putText(frame,'Plus Pitch',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
			cmd='P'
		elif l==6:
			cv2.putText(frame,'reposition',(0,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
		else :
			cv2.putText(frame,'reposition',(10,drawY), font, 2, (0,0,255), 3, cv2.LINE_AA)
	###################################################################################
        #show the windows
	if (number == 1):
		cv2.imshow('mask1',mask)
	elif (number == 2):
		cv2.imshow('mask2',mask)
	cv2.imshow('frame',frame)
	return cmd





def cv_drone():
	global cmd1
	global cmd2
	global drone_select
	while(1):
		try:	#an error comes if it does not find anything in window as it cannot find contour of max area
				#therefore this try error statement
			current_drone_frame = np.zeros((200,200,3),np.uint8)
			
			ret, frame = cap.read() #cap.read 비디오를 1프레임씩 읽음. 성공시 RET = TRUE 실패시 FALSE    
			frame=cv2.flip(frame,1) # 프레임을 좌우반전. 인자값이 0이면 상하반전
			kernel = np.ones((3,3),np.uint8)	#1로 초기화된 3x3 배열을 만든다. 자료형은 0~255사이
											#이커널은 마스킹할때 이미지를 좌에서 우로 쭈욱 훑는다. 즉 범위에
											#해당하는 값이있으면 훑으면서 1로 기록, 없으면 0
			cmd1.append(str(capture(frame,kernel,100,300,25,225,1)))#left
			cmd2.append(str(capture(frame,kernel,100,300,400,600,2)))#right
			#print(cmd1+cmd2)
			if (cmd1[-1]+cmd2[-1] != '-1-1'):
				frame_count(cmd1[-1]+cmd2[-1])
			cv2.putText(current_drone_frame,str(current_drone[abs(drone_select)%4]),(100,100), 		cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
			cv2.imshow('current_drone is',current_drone_frame)
			
		except Exception:
			#traceback.print_exc()
			pass
   		    # break
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as m1:
		m1.connect(('127.0.0.1',PORT1)) #1111 port
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as m2:
			m2.connect(('127.0.0.1',PORT2)) #2222 port
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as m3:
				m3.connect(('127.0.0.1',PORT3)) #3333 port
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as m4:
					m4.connect(('127.0.0.1',PORT4)) #4444 port

					receive1 = []
					receive1.append('0')
					receive2 = []
					receive2.append('0')
					receive3 = []
					receive3.append('0')
					receive4 = []
					receive4.append('0')
					
					dance = []
					dance.append('1000')
					t1 = threading.Thread(target=keep_listen1)
					t2 = threading.Thread(target=keep_listen2)
					t3 = threading.Thread(target=keep_listen3)
					t4 = threading.Thread(target=keep_listen4)
					t5 = threading.Thread(target=keep_send)
					#t6 = threading.Thread(target=drone_music)
					t7 = threading.Thread(target=cv_drone)
					t1.start()
					t2.start()
					t3.start()
					t4.start()
					t5.start()
					#t6.start()
					t7.start()
					print('Init Main Program')
					while (1):
						if (dance[-1] =='-1T' ):
							print('Take-off !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='1-1'): # Dance1 Check 7 Sync
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							time.sleep(1)
							dance.append('1000')
							print('End of Dance1 Going Back to Main Loop')
						elif (dance[-1] =='2-1'): #Dance2 
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							time.sleep(1)
							dance.append('1000')
							print('End of Dance2 Going Back to Main Loop')
						elif (dance[-1] =='3-1'): #Check 8 Sync
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							if(dance[-1]!='-15'):
								drone_sync()
							time.sleep(1)
							dance.append('1000')
							print('End of Dance3 Going Back to Main Loop')
						elif (dance[-1] =='-10'):
							print('Safe Landing !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='05'or dance[-1] =='451' or dance[-1] =='452' or dance[-1] =='453' or dance[-1] =='454' ):
							print('Minus Pitch !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='0P'or dance[-1] =='4P1' or dance[-1] =='4P2' or dance[-1] =='4P3' or dance[-1] =='4P4' ):
							print('Plus Pitch !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='0L'or dance[-1] =='4L1' or dance[-1] =='4L2' or dance[-1] =='4L3' or dance[-1] =='4L4' ):
							print('Minus Roll !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='0R'or dance[-1] =='4R1' or dance[-1] =='4R2' or dance[-1] =='4R3' or dance[-1] =='4R4'  ):
							print('Plus Roll !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='01'or dance[-1] =='411' or dance[-1] =='412' or dance[-1] =='413' or dance[-1] =='414' ):
							print('Turn Left !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='02'or dance[-1] =='421' or dance[-1] =='422' or dance[-1] =='423' or dance[-1] =='424' ):
							print('Turn Right !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='03'or dance[-1] =='431' or dance[-1] =='432' or dance[-1] =='433' or dance[-1] =='434'):
							print('Flip !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='-15'):
							print('Emergency Signal !! \n')
							time.sleep(1)
							dance.append('1000')
						elif (dance[-1] =='100'):
							print('ShutDown \n')
							time.sleep(1)
							m1.close()
							m2.close()
							m3.close()
							m4.close()
							break


except KeyboardInterrupt:
	m1.close()
	m2.close()
	m3.close()
	m4.close()
	cv2.destroyAllWindows()
	cap.release()    
	print("Closing...")
