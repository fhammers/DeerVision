import cv2
import numpy as np
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from thermography import CreateFrames

PROJECT_NAME = 'IR Thermal Processing'

def OnVidTrackbar(val):
    cap.set(cv2.CAP_PROP_POS_FRAMES, val)
    ret, frame = cap.read()
    view = CreateFrames(frame)
    cv2.imshow(PROJECT_NAME, view)
    return

def ShowVideo(URL, FPS=30):
    # Bind video file
    cap = cv2.VideoCapture(URL)
    VID_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create window
    cv2.namedWindow(PROJECT_NAME, cv2.WINDOW_AUTOSIZE)

    # Create trackbars
    cv2.createTrackbar('Frame', PROJECT_NAME, 0, VID_FRAMES, OnVidTrackbar)

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

def ShowImage(URL):

        # Create window
        cv2.namedWindow(PROJECT_NAME, cv2.WINDOW_AUTOSIZE)

        # Get image
        img = cv2.imread(URL)

        # Perform cv2 operations
        view = CreateFrames(img)

        cv2.imshow(PROJECT_NAME, view)
        cv2.waitKey(-1)

        # Release binds and destroy for clean exit
        cv2.destroyAllWindows()

def main():
    #destroy root tk window
    Tk().withdraw()

    # Video source path
    URL = askopenfilename() # Prompt for video selection
    fileSuffix = URL.split('.')[1]

    if str.upper(fileSuffix) == 'JPG':
        ShowImage(URL)
    else:
        ShowVideo(URL)

    #root.destroy() #destroy tkinter

    print("EXIT - clean")

if __name__ == "__main__":
    main()