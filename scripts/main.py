## main execution script, first run through
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from webodmAPI import WebODMAPI
import time

import os

status_codes = {
    "QUEUED": 10,
    "RUNNING": 20,
    "FAILED" : 30,
    "COMPLETED": 40,
    "CANCELED": 50
}


class DeerVision(Tk):
    def __init__(self):
        super(DeerVision, self).__init__()
         
        self.list_dir =  ""
        
        print(os.getcwd())
        #initialize tkinter window
        self.title("Deer Vision")
        self.minsize(640, 400)
        # self.configure(background='grey')
       

        self.labelFrame = ttk.LabelFrame(self, text="Select a directory")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        self.labelFrame.pack(padx=10, pady=20)
        self.text = None

        self.button()
        self.text = tk.Text(self.labelFrame, height=2, width = 30)
        self.text.grid(column = 1, row = 4)

        self.odm_API = WebODMAPI()
        # btn = Button(self.window, text="Browse", command = self.load_webODM, width = 10).pack()
    
    def button(self, text = ""):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File", command=self.load_file)
        self.button.grid(column = 1, row =1)

        self.sbt_button = ttk.Button(self.labelFrame, text= "Submit", command=self.load_webODM)
        self.sbt_button.grid(column = 1, row= 3)
        
        

    def load_file(self):
        file_name = filedialog.askdirectory(initialdir="./")
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = file_name)

        if file_name:
            self.list_dir = file_name
        else:
            raise ValueError("Invalid file directory")

        return self.list_dir

   
    def load_webODM(self):

        auth = self.odm_API.authenticate()
        
        if not auth:
            # handle lack of authentication
            return 
        
        self.odm_API.load_images(self.list_dir)

        #stitch images
        task_id = self.odm_API.stitch_images()

        #get progress
        if task_id:
            print("hello")
            self.get_status(task_id)

        self.odm_API.download_tif(task_id)

    def get_status(self, task_id):

        while True:
            self.text.delete(1.0,END)
            res = self.odm_API.get_stitch_status(task_id)
            if res['status'] == status_codes["COMPLETED"]:
                print("Task has completed!")
                self.text.insert(tk.END, "Task has completed!")
                break
            elif res['status'] == status_codes["FAILED"]:
                print("Task failed: {}".format(res))
                self.text.insert(tk.END, "Task failed: {}".format(res))
                sys.exit(1)
            elif res['status'] == status_codes["QUEUED"]:
                print("Task has been qeued")
                self.text.insert(tk.END, "Task has been qeued")
                time.sleep(3)
            else:
                print("Processing, hold on...")
                self.text.insert(tk.END, "Processing, hold on...")
                time.sleep(3)
            self.update_idletasks()



        #start file processing




def load_file():
    pass



# btn.grid(column=10, row=10)

if __name__ == "__main__":
    deer_process = DeerVision()
    deer_process.mainloop()

    # deer_process.start()



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
