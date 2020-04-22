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

def ExampleThreshold(URL, minThresh=200, maxThresh=255):

    img = cv2.imread(URL,0)

    ret,thresh1 = cv2.threshold(img,minThresh,maxThresh,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(img,minThresh,maxThresh,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(img,minThresh,maxThresh,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(img,minThresh,maxThresh,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(img,minThresh,maxThresh,cv2.THRESH_TOZERO_INV)

    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']

    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    return plt

def CreateFrames(frame, MINTHRESH=100, MAXTHRESH=255, RESIZE_FAC = 0.8):

    # Create canny
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, MINTHRESH, MAXTHRESH)

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