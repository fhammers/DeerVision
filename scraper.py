'''
Scraping images from Google Drive and then storing them for later use
'''
import os 
import shutil 

def scraper():
    source = '../deer-images' # change directory name here according to relative directory needed 
    destination = '../processed-deer-images' # same thing here
    
    dirs = os.listdir(source)

    for file in dirs:
        if file.split('.')[0][-1] == 'R':
            file_path = source + '/' + file
            shutil.copy(file_path, destination)
            
scraper()