#Martin Berger
#Advanced Lab
#This program will count the number of deer that appear in a stiched image


import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Ask user for file
picURL = askopenfilename()
image = cv2.imread(picURL,0)

# Set filtering parameters 
# Initialize parameter settiing using cv2.SimpleBlobDetector 
params = cv2.SimpleBlobDetector_Params() 
  
# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Set Area filtering parameters (Area in pixels)
params.filterByArea = True
params.minArea = 100
  
# Set Circularity filtering parameters (4*pi*Area/perimiter^2, circle = 1)
params.filterByCircularity = True 
params.minCircularity = 0.55
params.maxCircularity = 0.9
  
# Set Convexity filtering parameters 
params.filterByConvexity = True
params.minConvexity = 0.87
      
# Set inertia filtering parameters (How circular the object is: 1 = circle, 0 = line) 
params.filterByInertia = True
params.minInertiaRatio = 0.05
params.maxInertiaRatio = 0.6
  
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

print("Number of objects detected: " + str(len(keypoints)))  

# Show blobs 
cv2.imshow("Filtering Circular Blobs Only", blobs) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 