import numpy as np
import time
import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
from thermography import Thermography
from canvasViewer import CanvasImage
from matplotlib import pyplot as plt
import PIL
from PIL import Image, ImageTk


class PlayBack(Thermography):
    def __init__(self, windowTitle, thermo):
        #create thermo object
        self.thermo = thermo

        #store images from thermo object and w/h
        self.orig_img = thermo.originalImage
        self.image = self.orig_img
        self.imgWidth = self.image.shape[1]
        self.imgHeight = self.image.shape[0]

        #create master tkinter window
        self.master = Toplevel()
        self.master.title(windowTitle)

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        #create main frames
        self.topFrame = Frame(self.master)
        self.midFrameL = Frame(self.master)
        self.midFrameR = Frame(self.master)
        self.btmFrame = Frame(self.master)

        self.fontStyle = tkFont.Font(family="Lucida Grande", size=16)

        #deer label and number of blobs detected
        self.deerLabel = Label(self.topFrame, text = "Number of Deer:", font=self.fontStyle).\
                    grid(row= 0, column = 0, pady = 2)
        self.deerCount = Label(self.topFrame, text = str(self.thermo.getNumberBlobs()), font=self.fontStyle).\
                    grid(row =0, column = 1, pady = 2)
        
        #image canvas
        self.canvas = Canvas(self.midFrameL, width = self.imgWidth, height = self.imgHeight)
        self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.image))
        self.canvasImage = self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        #self.canvas = CanvasImage(self.midFrame, self.thermo.URL)  # create widget
        self.canvas.grid(row=0, column=0)

        self.viewLabel= Label(self.midFrameR, text = "View Selection").grid(row=0, column =1)
        
        self.viewSelector = Combobox(self.midFrameR, 
                            values=[
                                    "Thermal", 
                                    "Mask",
                                    "Blob",])
        self.viewSelector.current(0)
        self.viewSelector.grid(row=1, column=1)
        self.viewSelector.bind("<<ComboboxSelected>>", self.changeView)
    
        self.topFrame.grid(row=0)
        self.midFrameL.grid(row=1, column =0)
        self.midFrameR.grid(row=1, column =1)
        self.btmFrame.grid(row=3)

        self.master.mainloop()

    def changeView(self, event):
        view = self.viewSelector.get()
        if view == "Thermal":
            self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.thermo.getOriginalImage()))
        if view == "Mask":
            self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.thermo.getMaskImage()))
        if view == "Blob":
            self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.thermo.getBlobImage()))
        self.canvas.itemconfig(self.canvasImage, image = self.image)
            
def main():
    root = tkinter.Tk()
    root.withdraw()

    picURL = r"C:\Users\micha\OneDrive\Juniata\Advanced Lab\Thermal Content\Deer Images\DJI_0353_R.JPG"
    Thermo = Thermography(imageURL=picURL, colorMode = "red")
    PlayBack("Play Back", Thermo)
    
if __name__ == "__main__":
    main()