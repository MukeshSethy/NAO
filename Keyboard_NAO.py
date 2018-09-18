import serial
import time
from naoqi import ALProxy
from pynput import keyboard
ip = "192.168.0.6"
port = 9559
move = False
go = 0
motion = ALProxy("ALMotion", ip , port)
posture = ALProxy("ALRobotPosture", ip , port)
tts = ALProxy("ALTextToSpeech", ip , port)

position = posture.getPosture()
print "Posture = "
print position

def on_press(key):
	
	if key.char == 'w':
		go = 1
		wait = motion.post.moveTo(0.1 , 0 , 0)
	elif key.char == 's':
		go = -1
		wait = motion.post.moveTo(-0.1 , 0 , 0)
	elif key.char == 'q':
		tts.say("I   am    going   to   stand")
		posture.goToPosture("Stand" , 1.0)
		# motion.moveInit()
		move = True
	elif key.char == 'e':
		tts.say("I   am   going   to   sit")
		posture.goToPosture("Sit" , 1.0)
		move = False
	elif key.char == 'a':
		wait = motion.post.moveTo(0 , 0 , 0.174)
	elif key.char == 'd':
		wait = motion.post.moveTo(0 , 0 , -0.174)
	else:
		motion.stopMove()
	

def on_release(key):
    # print('{0} released'.format(13463634163key))
    motion.stopMove()
    if key == keyboard.Key.esc:
        # Stop listener
        print "Complete"
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
