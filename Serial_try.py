import serial
import time

port = "COM6"
baud = 9600
ch1 = 0
ch2 = 0
ch3 = 0
ser = serial.Serial(port, baud, timeout=1)
    # open the serial port
if ser.isOpen():
     print(ser.name + ' is open...')

t_end = time.time() + 20
data = []
ser.readline()
ser.flush()
while time.time() < t_end:
	data = ser.readline()
	print data
	i = 0
	j = 0
	k = 0
	while data[i] != 'B':
	 	i= i+1
	if i == 4:
		ch1 = 100*int(data[1]) + 10*int(data[2]) + int(data[3])
		
	elif i == 5:
		ch1 = 1000*int(data[1]) + 100*int(data[2]) + 10*int(data[3]) + int(data[4])
	print "ch1 = ",ch1
	while data[j] != 'C':
		j = j+1
	if j == 9:
		ch2 = 1000*int(data[5]) + 100*int(data[6]) + 10*int(data[7]) + int(data[8])
	elif j == 10:
		ch2 = 1000*int(data[6]) + 100*int(data[7]) + 10*int(data[8]) + int(data[9])
	print "\nch2 = ",ch2
	while data[k] != 'D':
		k = k+1
	if k == 14:
		ch3 = 1000*int(data[10]) + 100*int(data[11]) + 10*int(data[12]) + int(data[13])
	elif k == 15:
		ch3 = 1000*int(data[11]) + 100*int(data[12]) + 10*int(data[13]) + int(data[14])
	print "\nch3 = ",ch3
	# if ch1 < 1000 and ch1 > 800:
	# 	go = 1
	# 	motion.post.moveTo(0.05 , 0 , 0)
	# elif ch1 < 1900 and ch1 > 1800:
	# 	go = -1
	# 	motion.post.moveTo(-0.05 , 0 , 0)
	# elif ch3 > 1000 and ch3 < 1100:
	# 	motion.post.moveTo(0 , 0.05 , 0)
	# elif ch3 > 1900 and ch3 < 2100:
	# 	motion.post.moveTo(0 , -0.05 , 0)
	# else:
	# 	motion.stopMove()

print "Complete"
ser.close()