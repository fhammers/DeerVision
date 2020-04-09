import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


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
    ExampleThreshold(URL).show()

    #root.destroy() #destroy tkinter

    print("EXIT - clean")

if __name__ == "__main__":
    main()