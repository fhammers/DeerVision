# {tkinter}
from tkinter import *
from tkinter import filedialog, Button

# {WebODM}
from webodmAPI import WebODMAPI

# {Python}
import time
import os
from PIL import ImageTk, Image


status_codes = {
    "QUEUED": 10,
    "RUNNING": 20,
    "FAILED": 30,
    "COMPLETED": 40,
    "CANCELED": 50
}


class DeerVision(Tk):
    def __init__(self):
        super(DeerVision, self).__init__()

        self.list_dir = ""
        directory = os.getcwd()

        # initialize tkinter window
        self.title("Remote Intelligence")
        self.geometry("700x700")
        self.configure(background="white")
        self.resizable(False, False)

        # Adding RI logo to window
        self.RI_img = ImageTk.PhotoImage(Image.open(directory + "/images/RI_Logo.jpg"))
        self.iconLabel = Label(self, image=self.RI_img, bd=1)
        self.iconLabel.grid(column=0, row=0, columnspan=6)

        # Add frame for selecting images
        self.uploadFrame = LabelFrame(self, text="Begin Upload", bg="white", padx=50, pady=30)
        self.uploadFrame.grid(column=0, row=1)

        # Add buttons and padding
        self.newBtn = Button(self.uploadFrame, text="Select Folder", pady=10, width=15, command=self.load_file)
        self.newBtn.grid(column=0, row=1)
        self.dummyLabel1 = Label(self.uploadFrame, bd=1, bg="white")
        self.dummyLabel1.grid(column=0, row=4)
        self.webBtn = Button(self.uploadFrame, text="WebODM Settings", pady=10, width=15)
        self.webBtn.grid(column=0, row=7)
        self.dummyLabel2 = Label(self.uploadFrame, bd=1, bg="white")
        self.dummyLabel2.grid(column=0, row=10)
        self.viewStitchBtn = Button(self.uploadFrame, text="View Stitch", pady=10, width=15, state=DISABLED)
        self.viewStitchBtn.grid(column=0, row=13)
        self.dummyLabel3 = Label(self.uploadFrame, bd=1, bg="white")
        self.dummyLabel3.grid(column=0, row=16)
        self.submitBtn = Button(self.uploadFrame, text="Submit", pady=10, width=15, command=self.load_webODM)
        self.submitBtn.grid(column=0, row=19)

        self.odm_API = WebODMAPI()


    def load_file(self):
        file_name = filedialog.askdirectory(initialdir="./")
        self.label = Label(self.uploadFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=file_name)

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

        # stitch images
        task_id = self.odm_API.stitch_images()

        # get progress
        if task_id:
            print("hello")
            self.get_status(task_id)

        self.odm_API.download_tif(task_id)


    def get_status(self, task_id):
        while True:
            self.text.delete(1.0, END)
            res = self.odm_API.get_stitch_status(task_id)
            if res['status'] == status_codes["COMPLETED"]:
                print("Task has completed!")
                self.text.insert(END, "Task has completed!")
                break
            elif res['status'] == status_codes["FAILED"]:
                print("Task failed: {}".format(res))
                self.text.insert(END, "Task failed: {}".format(res))
                sys.exit(1)
            elif res['status'] == status_codes["QUEUED"]:
                print("Task has been qeued")
                self.text.insert(END, "Task has been qeued")
                time.sleep(3)
            else:
                print("Processing, hold on...")
                self.text.insert(END, "Processing, hold on...")
                time.sleep(3)
            self.update_idletasks()


if __name__ == "__main__":
    deer_process = DeerVision()
    deer_process.mainloop()

    # deer_process.start()

    ## start tkinkter root window
    ## gui calls here
    # startGUI()

    ##if gui is event driven then we need it in a loop to check for a key press to jump out of loop,
    # or tie it to a main function, I'll leave this to the programmer, maybe that event calls main.main()

    ##scraper scripts to separate thermal from non-theral files, I think we should have a checkbox option
    # for which images they would like stitched, thermal should be preset to true with non-thermals set as false
    # scrape images and pass them to webodm api
    # change output of scraper to be correct input for webODM api
    # webODM_container = scraper()

    # run webodm scripts based off gui selected parameters if there are any
    # webODMapi.post()

    # is there a way to check for stitch progress through api?

    # store returned objects
    # thermalTiff = webODMapi.request()

    # run tiff image through deer counter sequence, this should be a single call
    # deerImage = counter.findDeer()

    # get nuimber of deer found and present that image

    # have a button on gui that takes you to where new image where deer displayed is found

    # clean up tkinter and exit
