import time
import os
import threading

# tracker variables for naming
NUMBER_OF_CAMS = 3
NUMBER_OF_MODELS = 5 # number of models to be captured
usb = ['/dev/video0', '/dev/video2', '/dev/video4']
size = '352x288'
M = 0

# M_modelNum_V_camNum.jpg

## capture code
def capture(count, view):
	print 'currently capturing ' + usb[view]
	fname = 'M_' + str(count) + '_V_' + str(view) + '.jpg'
	os.system('fswebcam ' + fname + ' -r ' + size + ' -d ' + usb[view] + ' -p YUYV')

## capture 3 cameras, leap motion
def snap():
	# capture 3 cameras concurrently
	for V in range(NUMBER_OF_CAMS):
		x = threading.Thread(name='cam'+str(V), target=capture, args=(M, V,))
		# time.sleep(0.1)
		x.start()
		# capture(port, counter)

	# capture leap motion
	#TODO - SEE LEAP MOTION SAMPLE


for i in range(NUMBER_OF_MODELS):
	print '-------------------capturing M = ' + str(i) + ' -------------------'
	snap()
	time.sleep(3) #TO BE EDITED WITH LEAP MOTION
	M += 1
	raw_input("Press Enter to continue...")
print '---------------------completed ' + str(NUMBER_OF_MODELS) + ' captures-----------------------'
