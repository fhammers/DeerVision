#Martin Berger
#Advanced Lab
#This program will count the number of deer that appear in a stiched image


import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def counter(filepath = "blah"):
	# Hide root Tk window 
	root = Tk()
	root.withdraw()

	#Ask user for file
	picURL = askopenfilename()
	root.destroy()

	#store image path
	image = cv2.imread(picURL,0)
	
	# Set filtering parameters 
	# Initialize parameter settiing using cv2.SimpleBlobDetector 
	params = cv2.SimpleBlobDetector_Params() 
	
	# Change thresholds
	params.minThreshold = 50
	params.maxThreshold = 255

	# Set Area filtering parameters (Area in pixels)
	params.filterByArea = True
	params.minArea = 300
	
	# Set Circularity filtering parameters (4*pi*Area/perimiter^2, circle = 1)
	params.filterByCircularity = True 
	params.minCircularity = 0.45
	params.maxCircularity = 0.9
	
	# Set Convexity filtering parameters 
	params.filterByConvexity = True
	params.minConvexity = 0.95
		
	# Set inertia filtering parameters (How circular the object is: 1 = circle, 0 = line) 
	params.filterByInertia = True
	params.minInertiaRatio = 0.05
	params.maxInertiaRatio = 0.8
	
	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
		detector = cv2.SimpleBlobDetector(params)
	else : 
		detector = cv2.SimpleBlobDetector_create(params) 
		
	# Detect blobs 
	keypoints = detector.detect(image) 
	
	# Draw blobs on our image as red circles 
	blank = np.zeros((1, 1))  
	blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),
				cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
	
	number_of_blobs = len(keypoints) 
	# text = "Number of Circular Blobs: " + str(len(keypoints)) 
	# cv2.putText(blobs, text, (20, 550), 
	#             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2) 

	print("Number of objects detected: " + str(number_of_blobs))  

	# Show blobs 
	cv2.imshow("Filtering Circular Blobs Only", blobs) 
	cv2.imwrite("test.jpg", blobs)
	cv2.waitKey(0) 
	cv2.destroyAllWindows() 

counter()
