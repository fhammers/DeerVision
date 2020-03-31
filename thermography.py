# 
# Thermal Imagine Script
# Michael Young
# Advanced Lab
# 

import cv2
import numpy as np
import time
import tkinter as Tk
from tkinter.filedialog import askopenfilename

PROJECT_NAME = 'IR Thermal Processing'

# Image resizes
RESIZE_FAC = 0.8

# Canny delta thresholds
CANNY_MAX = 255
maxThresh = 250
minThresh = 100

# Playback var
FPS = 30

#Tk().withdraw()

# Video source path
vidURL = askopenfilename() # Prompt for video selection
#vidURL = r'C:\Users\Michael\OneDrive\Juniata\Advanced Lab\IR\video\test.mov'

# Bind video file
cap = cv2.VideoCapture(vidURL)

VID_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

def OnTrackbar(val):
    cap.set(cv2.CAP_PROP_POS_FRAMES, val)
    ret, frame = cap.read()
    view = CreateFrames(frame)
    cv2.imshow(PROJECT_NAME, view)
    return

def CreateFrames(frame):

    # Create canny
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, minThresh, maxThresh)

    # Negative frame (bits flipped)
    neg = ~frame

    # Convert canny to correct color dimensionality
    canny3d = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    # Overlay canny with original
    added = cv2.addWeighted(frame, 0.5, canny3d, 0.5, 1)

    # Resize frames to the correct size
    frame = cv2.resize(frame, None, fx = RESIZE_FAC, fy = RESIZE_FAC)
    neg = cv2.resize(neg, None, fx= RESIZE_FAC, fy= RESIZE_FAC)
    canny3d = cv2.resize(canny3d, None, fx = RESIZE_FAC, fy = RESIZE_FAC)
    added = cv2.resize(added, None, fx = RESIZE_FAC, fy = RESIZE_FAC)

    # Create stacked views
    stack1 = np.hstack((frame, neg))
    stack2 = np.hstack((added, canny3d))
    stacked = np.vstack((stack1, stack2))

    # Update stacked view
    return stacked

# Create window
cv2.namedWindow(PROJECT_NAME, cv2.WINDOW_AUTOSIZE)

# Create trackbars
cv2.createTrackbar('Frame', PROJECT_NAME, 0, VID_FRAMES, OnTrackbar)


while(True):

    # Check for user input during playback
    key = cv2.waitKey(1)

    if key == ord('q'): #quits
        break

    if key == ord('p'): #pauses
        cv2.waitKey(-1) #waits until another key is pressed

    # Get next frame from feed
    ret, frame = cap.read()

    # Perform cv2 operations
    view = CreateFrames(frame)

    cv2.imshow(PROJECT_NAME, view)

    # FPS Controller (kinda)
    time.sleep(1/FPS)


# Release binds and destroy for clean exit
cap.release()
cv2.destroyAllWindows()

print("Finished")
