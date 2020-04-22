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

class Thermography():

	def __init__(self, URL, colorMode = "white"):

		self.URL = URL
		self.colorMode = colorMode
		self.originalImage = cv2.imread(URL)
		self.maskImage = ""
		self.blobImage = ""
		self.number_of_blobs = 0
		self.colorParam = True
		self.areaParam = False
		self.circularParam = False
		self.convexParam = False
		self.inertialParam = False
		self.params = cv2.SimpleBlobDetector_Params()

	def setUpParams(self):
		# Set filtering parameters 
		# Initialize parameter settiing using cv2.SimpleBlobDetector 
		#params = cv2.SimpleBlobDetector_Params() 
		
		# Change thresholds
		self.params.minThreshold = 10
		self.params.maxThreshold = 255

		# Set Color filtering parameters
		self.params.filterByColor = self.colorParam
		self.params.blobColor = 255

		# Set Area filtering parameters (Area in pixels)
		self.params.filterByArea = self.areaParam
		self.params.minArea = 3
		
		# Set Circularity filtering parameters (4*pi*Area/perimiter^2, circle = 1)
		self.params.filterByCircularity = self.circularParam 
		self.params.minCircularity = .2
		self.params.maxCircularity = 0.9
		
		# Set Convexity filtering parameters 
		self.params.filterByConvexity = self.convexParam
		self.params.minConvexity = 0.1
			
		# Set inertia filtering parameters (How circular the object is: 1 = circle, 0 = line) 
		self.params.filterByInertia = self.inertialParam
		self.params.minInertiaRatio = 0.01
		self.params.maxInertiaRatio = 0.99

		return

	def mask(self):

		# Creating a mask from red pixels
		image = self.originalImage.copy()
		cvrtColorImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# Sets the color that is being masked using HSV color format
		
		if self.colorMode == "red": 
			mask = cv2.inRange(image, (0,50,200), (50,180,255)) #Red
		if self.colorMode == "white":
			mask = cv2.inRange(cvrtColorImage, (0,0,200), (70,3,255)) #White

		result = cv2.bitwise_and(image, image, mask=mask)
		self.maskImage = result

		return 

	def counter(self): 
		
		# Create a detector with the parameters
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3 :
			detector = cv2.SimpleBlobDetector(self.params)
		else : 
			detector = cv2.SimpleBlobDetector_create(self.params) 
			
		# Detect blobs 
		keypoints = detector.detect(self.maskImage) 
		
		# Draw blobs on our image as red circles 
		blank = np.zeros((1, 1))  
		self.blobImage = cv2.drawKeypoints(self.originalImage, keypoints, blank, (0, 0, 255),
					cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
		
		self.number_of_blobs = len(keypoints) 
  
		return

	def process(self):
		self.setUpParams()
		self.mask()
		self.counter()

		stack1 = np.hstack((self.originalImage, self.maskImage))
		stack2 = np.hstack((self.blobImage, self.maskImage))
		stacked = np.vstack((stack1, stack2))

		return stacked


def main():
		# Hide root Tk window 
	root = Tk()
	root.withdraw()

	# Ask user for file
	picURL = askopenfilename()
	root.destroy()

	try:
		# counter(picURL)
		thermal = Thermography(picURL)
		cv2.imshow("Stacked", thermal.process())
		cv2.waitKey(0)

	except :
		print("Unexpected error:", sys.exc_info())

if __name__ == "__main__":
	main()