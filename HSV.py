import argparse
from naoqi import ALProxy
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

max_bin = 255
min_bin = 0
hmin = 0
hmax = 255
smin = 0
smax = 255
vmin = 0
vmax = 255

trackbar = ['thres_min' , 'thres_max' , 'H_min' , 'H_max' , 'S_min' , 'S_max' , 'V_min' , 'V_max']

def main(robot_IP, robot_PORT=9559):
	# ----------> Connect to robot <----------
	video = ALProxy("ALVideoDevice", robot_IP, robot_PORT)
	# ----------> <----------
	# Gets list of available camera indexes.
	print 'getCameraIndexes():', video.getCameraIndexes()
	# return [0,1] or [0,1,2]. Xtion Pro Live
	
	for num in video.getCameraIndexes():
		print '------------------'
		print 'Camera Index:', num
		print 'Camera Name:', video.getCameraName(num)
		print 'Camera Model:', video.getCameraModel(num)
		print 'Camera Frame Rate:', video.getFrameRate(num)
		print 'Camera Resolution:', video.getResolution(num)

	subscribers = video.getSubscribers()
	for s in range(0 , len(subscribers)):
		print subscribers[s]
		video.unsubscribe(subscribers[s])
	capture = video.subscribeCamera("Test" , 1 , 1 , 13 , 10)
	width = 320
	height = 240
	image = np.zeros((height , width , 3) , np.uint8)

	# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

	cv2.namedWindow("THRESHOLD" , cv2.WINDOW_NORMAL)
	cv2.createTrackbar("thres_max" , "THRESHOLD" , max_bin , 255 , change)
	cv2.createTrackbar("thres_min" , "THRESHOLD" , min_bin , 255 , change)
	cv2.createTrackbar("H_min" , "THRESHOLD" , hmin , 255 , change)
	cv2.createTrackbar("H_max" , "THRESHOLD" , hmax , 255 , change)
	cv2.createTrackbar("S_min" , "THRESHOLD" , smin , 255 , change)
	cv2.createTrackbar("S_max" , "THRESHOLD" , smax , 255 , change)
	cv2.createTrackbar("V_min" , "THRESHOLD" , vmin , 255 , change)
	cv2.createTrackbar("V_max" , "THRESHOLD" , vmax , 255 , change)
	change(0)

	while True:
		result = video.getImageRemote(capture)
		if result == None:
			print 'cannot capture.'
			video.releaseImage("Test")
		elif result[6] == None:
			print 'No image data string'
		else:
			values = map(ord , list(result[6]))
			i = 0
			for y in range(0 , height):
				for x in range(0 , width):
					image.itemset((y , x , 0) , values[i + 0])
					image.itemset((y , x , 1) , values[i + 1])
					image.itemset((y , x , 2) , values[i + 2])
					i += 3

			
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			hsv = cv2.cvtColor(image , cv2.COLOR_BGR2HSV)
			# cv2.imshow("HSV" , hsv)
			# cv2.imshow("Image" , image)
			lower = np.array([change(2) , change(4) , change(6)])
			upper = np.array([change(3) , change(5) , change(7)])
			ret,thresh1 = cv2.threshold(gray , change(0) , change(1) , cv2.THRESH_BINARY)
			mask = cv2.inRange(hsv , lower , upper)
			res = cv2.bitwise_and(image , image , mask= mask)
			# ret,thresh2 = cv2.threshold(image,120,125,cv2.THRESH_BINARY_INV)
			# ret,thresh3 = cv2.threshold(image,127,255,cv2.THRESH_TRUNC)
			# ret,thresh4 = cv2.threshold(image,127,255,cv2.THRESH_TOZERO)
			# ret,thresh5 = cv2.threshold(image,127,255,cv2.THRESH_TOZERO_INV)

			titles = ['Original Image','GREY to BINARY','MASK','HSV to BINARY','HSV','TOZERO_INV']
			images = [image , thresh1 , res , mask , hsv]
			# , thresh2, thresh3, thresh4, thresh5]

			for i in xrange(5):
				cv2.imshow(str(titles[i]) , images[i])

		if cv2.waitKey(10) == 27:
			break
	print "Finished"
	video.releaseImage("Test")
	video.unsubscribe("Test")
	cv2.destroyAllWindows() 

def change(num):
	win = "THRESHOLD"
	if num >= 0 and num <= 7:
		return cv2.getTrackbarPos(str(trackbar[num]) , win)
	# if num == 0:
	# 	return cv2.getTrackbarPos("thres_min" , "THRESHOLD") 
	# elif num == 1:
	# 	return cv2.getTrackbarPos("thres_max" , "THRESHOLD")
	# elif num == 2:
	# 	return cv2.getTrackbarPos("H_min" , "THRESHOLD")
	# elif num == 3:
	# 	return cv2.getTrackbarPos("H_max" , "THRESHOLD")
	# elif num == 4:
	# 	return cv2.getTrackbarPos("S_min" , "THRESHOLD")
	# elif num == 5:
	# 	return cv2.getTrackbarPos("S_max" , "THRESHOLD")
	# elif num == 6:
	# 	return cv2.getTrackbarPos("V_min" , "THRESHOLD")
	# elif num == 7:
	# 	return cv2.getTrackbarPos("V_max" , "THRESHOLD")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.4", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)