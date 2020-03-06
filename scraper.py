import os
from tkinter import filedialog
from tkinter import *

#root = Tk()

Tk().withdraw()

dir = filedialog.askdirectory()

entries = os.listdir(dir)

for entry in entries:
    print(entry)







