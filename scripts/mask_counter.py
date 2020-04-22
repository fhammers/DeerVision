# Martin Berger
# Advanced Lab
# This program will count the number of deer that appear in a stiched image
# It uses a mask to filter to red spots (deer or other high heat objects)
# then uses SimpleBlobDetector from OpenCV to count the number of deer in the
# image.

import cv2 as cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def mask(URL):
	# Grab file
	# image = cv2.imread("C:\\Users\\Martin Berger\\Desktop\\DJI_0315_R.jpg")
	image = cv2.imread(URL)

	# Creating a mask from red pixels
	result = image.copy()
	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Sets the color that is being masked using HSV color format
	
	# mask = cv2.inRange(image, (0,50,200), (50,180,255)) #Red
	mask = cv2.inRange(image, (0,0,200), (70,3,255)) #White
	result = cv2.bitwise_and(result, result, mask=mask)
	# blur = cv2.GaussianBlur(result,(3,3),0)
	# mask_blur = cv2.GaussianBlur(mask,(7,7),0)

	# cv2.imshow('mask_blur', mask_blur)
	cv2.imshow('mask', mask)
	# cv2.imshow('result', blur)
	cv2.waitKey()

	return mask

def counter(URL): 
	#image = cv2.imread(URL)
	image = mask(URL)

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
	params.minArea = 3
	
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
	keypoints = detector.detect(image) 
	
	# Draw blobs on our image as red circles 
	blank = np.zeros((1, 1))  
	blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),
				cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
	
	number_of_blobs = len(keypoints) 

	# print("Number of deer detected: " + str(number_of_blobs))  
	return(blobs,number_of_blobs)

	# Show blobs 
	# cv2.imshow("Final Count", blobs) 
	# cv2.imwrite("test.jpg", blobs)
	# cv2.waitKey(0) 
	# cv2.destroyAllWindows() 

def main():
		# Hide root Tk window 
	root = Tk()
	root.withdraw()

	# Ask user for file
	picURL = askopenfilename()
	root.destroy()
	try:
		# counter(picURL)
		image,deer_num = counter(picURL)

		# Display the image and the number of deer counted
		cv2.imshow("Final Count", image) 
		cv2.imwrite("test.jpg", image)
		print("Number of deer detected: " + str(deer_num))

		cv2.waitKey(0) 
		cv2.destroyAllWindows() 
		

	except :
		print("Unexpected error:", sys.exc_info())

if __name__ == "__main__":
	main()
