import os 
import shutil 
import logging
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import Open
from tkinter.filedialog import SaveAs

def setUpLogs():
    logger = logging.getLogger("sorter.log")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    logger.addHandler(ch)

def scraper():

    # Hide root TK window
    root = Tk()
    root.withdraw()

    source = askdirectory() #'../deer-images' change directory name here according to relative directory needed 
    destination = askdirectory() #'../processed-deer-images' # same thing here
    
    root.destroy() # destroy Tk windows - tidy cleanup

    dirs = os.listdir(source)

    for file in dirs:
        if file.split('.')[-2][-1] == 'R':
            file_path = source + '/' + file
            shutil.copy(file_path, destination)

def sortImages(src):

    # absolute path where images are stored that need to be sorted
    directory = os.path.abspath(src)
    logging.info('Absolute path = ' + directory)

    #change operating directory to specified folder
    os.chdir(directory)

    # check if a "thermal" and "non-thermal" folder already exist
    # if not, create them
    if not os.path.exists('thermal'):
        os.mkdir('thermal')
    if not os.path.exists('non-thermal'):
        os.mkdir('non-thermal')

    destination = directory

    filesFound = 0
    thermalFiles = 0
    nonThermalFiles = 0

    for folder, subdirs, files in os.walk(directory, topdown=False):
        
        logging.info(' In subdirectory: {0}'.format(folder))

        for filename in files:
            if filename.split('.')[-1] == 'jpg' or 'JPG':
                if filename.split('.')[-2][-1] == 'R':
                    file_path = os.path.join(folder, filename)
                    newFileName = '{}R.jpg'.format(filesFound)
                    #shutil.move(file_path, os.path.join(destination, 'thermal', newFileName))
                    thermalFiles+=1
                else:
                    file_path = os.path.join(folder, filename)
                    newFileName = '{}.jpg'.format(filesFound)
                    #shutil.move(file_path, os.path.join(destination, 'non-thermal', newFileName))
                    nonThermalFiles+=1
                
            else:
                logging.debug('Filename: {0} - Split: {1}'.format(filename, filename.split('.')[-2][-1]))
            filesFound+=1

        logging.info('Sorted {0} files: {1} thermal | {2} non-thermal'.format(thermalFiles+nonThermalFiles, thermalFiles, nonThermalFiles))
    
def main():

     # Hide root TK window
    root = Tk()
    root.withdraw()

    source = askdirectory() #'../deer-images' change directory name here according to relative directory needed 
    #destination = askdirectory() #'../processed-deer-images' # same thing here
    
    root.destroy() # destroy Tk windows - tidy cleanup

    setUpLogs()
    sortImages(source)

if __name__ == "__main__":
    main()