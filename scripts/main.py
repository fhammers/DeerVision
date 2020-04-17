## main execution script, first run through
from tkinter import *
from tkinter import filedialog







class DeerVision:
    def __init__(self):
         
        self.list_dir =  ""


        #initialize tkinter window
        self.window = Tk()
        self.window.title("Deer Vision")
        self.window.geometry('600x200')
        btn = Button(self.window, text="Browse", command = self.load_file, width = 10).pack()


    def start(self):
        self.window.mainloop()


    
    def load_file(self):
        file_name = filedialog.askdirectory()

        if file_name:
            self.list_dir = file_name




def load_file():
    pass



# btn.grid(column=10, row=10)

if __name__ == "__main__":
    deer_process = DeerVision()

    

    deer_process.start()











def main():
    pass

    ## start tkinkter root window
    ## gui calls here
    #startGUI()

    ##if gui is event driven then we need it in a loop to check for a key press to jump out of loop,
    #or tie it to a main function, I'll leave this to the programmer, maybe that event calls main.main()

    ##scraper scripts to separate thermal from non-theral files, I think we should have a checkbox option
    #for which images they would like stitched, thermal should be preset to true with non-thermals set as false
    #scrape images and pass them to webodm api
    # change output of scraper to be correct input for webODM api
    #webODM_container = scraper()

    #run webodm scripts based off gui selected parameters if there are any
    #webODMapi.post()

    #is there a way to check for stitch progress through api?

    #store returned objects
    #thermalTiff = webODMapi.request()

    #run tiff image through deer counter sequence, this should be a single call
    #deerImage = counter.findDeer()

    #get nuimber of deer found and present that image

    #have a button on gui that takes you to where new image where deer displayed is found

    #clean up tkinter and exit