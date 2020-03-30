'''
Scraping images from Google Drive and then storing them for later use
'''
import os 
import shutil 
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import Open
from tkinter.filedialog import SaveAs

def scraper():
    source = askdirectory() #'../deer-images' change directory name here according to relative directory needed 
    destination = askdirectory() #'../processed-deer-images' # same thing here
    
    dirs = os.listdir(source)

    for file in dirs:
        if file.split('.')[0][-1] == 'R':
            file_path = source + '/' + file
            shutil.copy(file_path, destination)
            
scraper()