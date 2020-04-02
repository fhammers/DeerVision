#Martin Berger
#Advanced Lab
#This program will count the number of deer that appear in a stiched image


import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def counter(filepath = "blah"):
	# Hide root Tk window 
	# root = Tk()
	# root.withdraw()

	# #Ask user for file
	# picURL = askopenfilename()
	# root.destroy()

	# #store image path
	image = cv2.imread("C:\\Users\\Martin Berger\\Desktop\\DJI_0693_R.jpg")
	mask_blur = image

	# Creating a mask from red pixels
	result = image.copy()
	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(image, (0,100,170), (70,255,255))
	result = cv2.bitwise_and(result, result, mask=mask)
	blur = cv2.GaussianBlur(result,(3,3),0)
	mask_blur = cv2.GaussianBlur(mask,(7,7),0)

	cv2.imshow('mask_blur', mask_blur)
	cv2.imshow('mask', mask)
	# cv2.imshow('result', blur)
	cv2.waitKey()
	
	# Set filtering parameters 
	# Initialize parameter settiing using cv2.SimpleBlobDetector 
	params = cv2.SimpleBlobDetector_Params() 
	
	# Change thresholds
	params.minThreshold = 10
	params.maxThreshold = 255

	# Set Color filtering parameters
	params.filterByColor = True
	params.blobColor = 255

	# Set Area filtering parameters (Area in pixels)
	params.filterByArea = True
	params.minArea = 2
	
	# Set Circularity filtering parameters (4*pi*Area/perimiter^2, circle = 1)
	params.filterByCircularity = False 
	params.minCircularity = .2
	params.maxCircularity = 0.9
	
	# Set Convexity filtering parameters 
	params.filterByConvexity = False
	params.minConvexity = 0.1
		
	# Set inertia filtering parameters (How circular the object is: 1 = circle, 0 = line) 
	params.filterByInertia = False
	params.minInertiaRatio = 0.01
	params.maxInertiaRatio = 0.99
	
	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
		detector = cv2.SimpleBlobDetector(params)
	else : 
		detector = cv2.SimpleBlobDetector_create(params) 
		
	# Detect blobs 
	keypoints = detector.detect(mask) 
	
	# Draw blobs on our image as red circles 
	blank = np.zeros((1, 1))  
	blobs = cv2.drawKeypoints(mask, keypoints, blank, (0, 0, 255),
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
