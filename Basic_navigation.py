import naoqi
import time
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
                    
# create python module
# Python documentation will apear on web browser documentation
class myModule(ALModule):
	def pythondatachanged(self, strVarName, value, strMessage):
		proxy.unsubscribeToEvent("Navigation/SafeNavigator/BlockingObstacle" , "pythonModule")
		print strVarName , " = " , value
		tts.say("Obstacle Detected")
		proxy.subscribeToEvent("Navigation/SafeNavigator/BlockingObstacle","pythonModule", "pythondatachanged")
					# proxy.subscribeToEvent("SonarLeftDetected","pythonModule", "pythondatachanged")

                    
broker = ALBroker("pythonBroker","192.168.0.3" , 139 , "192.168.0.4",9559)
                    
# call method
try:
	pythonModule = myModule("pythonModule")    # don't forget to have the same module name and instance name
	proxy = ALProxy("ALMemory")
	nav = ALProxy("ALNavigation")
	sonar = ALProxy("ALSonar")
	motion = ALProxy("ALMotion")
	posture = ALProxy("ALRobotPosture")
	tts = ALProxy("ALTextToSpeech")
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
	motion.setExternalCollisionProtectionEnabled("Move" , True)
	motion.setOrthogonalSecurityDistance(0.3)
	motion.setTangentialSecurityDistance(-0.02)
	# proxy.raiseMicroEvent("val",0)
	proxy.subscribeToEvent("Navigation/SafeNavigator/BlockingObstacle","pythonModule", "pythondatachanged")
	# proxy.raiseMicroEvent("val",1)
except Exception,e:
	print "error behavior"
	print e
	

t_end = time.time() + 50

while time.time() < t_end:
	motion.moveTo(0.01 , 0 , 0)

tts.say("Time limit reached.")
# sonar.unsubscribe("myApplication")
posture.goToPosture("Crouch", 1.0 )
motion.setStiffnesses('Body' , 0.3)