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
        self.deerFound = StringVar()
        self.areaScaleValue = StringVar()
        self.enableBlobs = BooleanVar()

        #store images from thermo object and w/h
        self.orig_img = self.thermo.originalImage
        self.image = self.thermo.originalImage
        self.imgWidth = self.thermo.originalImage.shape[1]
        self.imgHeight = self.thermo.originalImage.shape[0]

        #create master tkinter window
        self.master = Toplevel()
        self.master.title(windowTitle)

        #row configuration
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        #create main frames
        self.topFrame = Frame(self.master)
        self.midFrameL = Frame(self.master)
        self.midFrameR1 = Frame(self.master)
        self.midFrameR2 = Frame(self.master)
        self.btmFrame = Frame(self.master)

        #font style
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=16)

        #deer label and number of blobs detected
        self.deerLabel = Label(self.topFrame, text = "Number of Deer:", font=self.fontStyle).\
                    grid(row= 0, column = 0, pady = 2)
        self.deerCount = Label(self.topFrame, textvariable = self.deerFound, font=self.fontStyle).\
                    grid(row =0, column = 1, pady = 2)
        self.deerFound.set(str(self.thermo.getNumberBlobs()))

        #image canvas
        self.canvas = Canvas(self.midFrameL, width = self.imgWidth, height = self.imgHeight)
        self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.image))
        self.canvasImage = self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        #self.canvas = CanvasImage(self.midFrame, self.thermo.URL)  # create widget
        self.canvas.grid(row=0, column=0)

        #mask options labelframe
        self.maskMenu = LabelFrame(self.midFrameR1, text = "Mask Options")
        self.maskMenu.grid(row=0, column=0)

        self.blobsCheck = Checkbutton(self.maskMenu, text = "Enable Blobs", \
                                            variable = self.enableBlobs, command = self.changeView)
        self.blobsCheck.grid(row=1, column =0)

        self.blobScale = Scale(self.maskMenu, from_= 1, to = 25, command = self.changeView)
        self.blobScale.grid(row=2, column =0)
        self.blobScaleValue = Label(self.maskMenu, textvariable = self.areaScaleValue)
        self.blobScaleValue.grid(row=2, column=1)

        #view selector
        self.viewLabel= Label(self.midFrameR2, text = "View Selection").grid(row=1, column =0)
        
        self.viewSelector = Combobox(self.midFrameR2, 
                            values=["Thermal", 
                                    "Mask",])
        self.viewSelector.grid(row=2, column=0)
        self.viewSelector.bind("<<ComboboxSelected>>", self.changeView)

        #initialize parameters
        self.areaScaleValue.set(str(int(self.blobScale.get())))
        self.blobScale.set(self.thermo.minAreaParam)
        self.viewSelector.current(0)

        #frame placement
        self.topFrame.grid(row=0)
        self.midFrameL.grid(row=1, column =0, rowspan =2, padx =(15,15))
        self.midFrameR1.grid(row=1, column =1, padx =(15,15))
        self.midFrameR2.grid(row=2, column=1,padx =(15,15))
        self.btmFrame.grid(row=3, pady=5)

        self.master.mainloop()

    def update(self):
        view = self.viewSelector.get()
        self.thermo.process()
        self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.thermo.getImage()))
        self.canvas.itemconfig(self.canvasImage, image = self.image)
        self.deerFound.set(str(self.thermo.getNumberBlobs()))
        self.areaScaleValue.set(str(int(self.blobScale.get())))

    def changeView(self, event=""):
        self.thermo.setView(self.viewSelector.get())
        self.thermo.setBlobArea(int(self.blobScale.get()))
        self.thermo.setBlob(self.enableBlobs.get())
        self.update()
            
def main():
    root = tkinter.Tk()

    picURL = r"C:\Users\micha\OneDrive\Juniata\Advanced Lab\Thermal Content\Deer Images\DJI_0353_R.JPG"
    Thermo = Thermography(imageURL=picURL, colorMode = "red")
    PlayBack("Play Back", Thermo)

    
if __name__ == "__main__":
    main()