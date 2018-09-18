from naoqi import ALProxy
import math
import time
import sys

ip = "192.168.43.88"
move = False
threshold = 0.35

motion = ALProxy("ALMotion", ip , 9559)
posture = ALProxy("ALRobotPosture", ip , 9559)
tts = ALProxy("ALTextToSpeech", ip , 9559)
sonar = ALProxy("ALSonar", ip , 9559)
memory = ALProxy("ALMemory", ip, 9559)
navigate = ALProxy("ALNavigation", ip , 9559)

print "Connection Successful \n"
position = posture.getPosture()
print "Posture = "
print position

if position == 'Stand' or position == 'StandInit':
	move = True	
elif position == 'Sit' or position == 'Crouch' :
	posture.goToPosture("Stand" , 1.0)
	move = True
elif position != 'Sit':
	posture.goToPosture("Sit", 1.0 )
	posture.goToPosture("Stand", 1.0 )
	move = True

if move == True:
	tts.say("Start")
	motion.moveInit()
else:
	tts.say("Failed to stand")
	sys.exit("Failed to stand")
time.sleep(2)
t_end = time.time() + 60
sonar.subscribe("myApplication")

ls = "Device/SubDeviceList/US/Left/Sensor/Value"
rs = "Device/SubDeviceList/US/Right/Sensor/Value"

while time.time() < t_end:
	# print 'LEFT = '
	# print left
	# print 'RIGHT = '
	# print right
	left = memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
	right = memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")

	if left > threshold and right > threshold:
		id = motion.post.moveTo(0.05 , 0 , 0)
		motion.wait(id,0)
	elif left <= threshold and right > threshold:
		print 'GO RIGHT'
		id = motion.post.moveTo(0 , 0 , -3.1415/18)
		motion.wait(id, 0)
	elif left > threshold and right <= threshold:
		print 'GO LEFT'
		id = motion.post.moveTo(0 , 0 , 3.1415/18)
		motion.wait(id, 0)
	else:
		moveRight = True
		for i in range(3):
			motion.moveTo(0 , 0.2 , 0)
			time.sleep(0.5)
			left = memory.getData(ls)
			right = memory.getData(rs)
			if left > threshold or right > threshold:
				moveRight = False
				break
		if moveRight == True:
			for i in range(6):
				motion.moveTo(0 , -0.2 , 0)
				time.sleep(0.5)
				left = memory.getData(ls)
				right = memory.getData(rs)
				if left > threshold or right > threshold:
					break
		left = memory.getData(ls)
		right = memory.getData(rs)
		if left <= threshold and right <= threshold:
			tts.say("Obstacle too big!")
			sys.exit("Obstacle too big")

tts.say("Time limit reached.")
sonar.unsubscribe("myApplication")
posture.goToPosture("Rest", 1.0 )