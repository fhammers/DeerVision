# {tkinter}
from tkinter import *
from tkinter import filedialog, Button, messagebox

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

        # flag to control upload frame
        self.uploadFrameState = "disable"

        # WebODM Api Call
        self.odm_API = WebODMAPI()

        self.list_dir = ""
        directory = os.getcwd()

        # global flag to hide widget
        self.enableDropDown = False

        # initialize tkinter window
        self.title("Remote Intelligence")
        self.geometry("700x700")
        self.configure(background="white")
        self.resizable(False, False)

        # project name
        self.project_name = ""

        # Adding RI logo to window
        self.RI_img = ImageTk.PhotoImage(Image.open(directory + "/images/RI_Logo.jpg"))
        self.iconLabel = Label(self, image=self.RI_img, bd=1)
        self.iconLabel.grid(column=0, row=0, columnspan=6)

        # Add initial frame
        self.initFrame = LabelFrame(self, text="Project Details", bg="white", padx=50, pady=30)
        self.initFrame.grid(column=2, row=1)

        # Add buttons to initial frame
        self.createProjectBtn = Button(self.initFrame, text="Create New Project", pady=10, width=30,
                                       command=self.createNewProject)
        self.createProjectBtn.grid(column=0, row=1)
        self.dummyLabel1 = Label(self.initFrame, bd=1, bg="white")
        self.dummyLabel1.grid(column=0, row=4)
        self.webBtn = Button(self.initFrame, text="WebODM Settings", pady=10, width=30)
        self.webBtn.grid(column=0, row=7)
        self.dummyLabel2 = Label(self.initFrame, bd=1, bg="white")
        self.dummyLabel2.grid(column=0, row=10)
        self.addTask = Button(self.initFrame, text="Add New Task To Existing Project", pady=10, width=30,
                              command=self.uploadProjectHelper)
        self.addTask.grid(column=0, row=13)
        dummyLabel3 = Label(self.initFrame, bd=1, bg="white")
        dummyLabel3.grid(column=0, row=16)
        viewStitchBtn = Button(self.initFrame, text="View Stitched Image", pady=10, width=15, state=DISABLED)
        viewStitchBtn.grid(column=0, row=19)

    def createNewProject(self):

        def submitNewProject():
            project_name = name.get("1.0", END)
            messagebox.showinfo("Success", "Created new project: " + project_name)
            self.project_name = project_name
            #self.odm_API.create_new_project(self, project_name)
            newProjectWindow.destroy()
            self.uploadProject()

        newProjectWindow = Toplevel()

        # Initialize window
        newProjectWindow.title("Create New Project")
        newProjectWindow.geometry("500x300")
        newProjectWindow.configure(background="white")
        newProjectWindow.resizable(False, False)

        # Create input field
        Label(newProjectWindow, text=" Project Name", bg="white").grid(column=1, row=1, pady=20, padx=20)
        name = Text(newProjectWindow, height=1, width=30, borderwidth=5)
        name.grid(column=2, row=1)
        Label(newProjectWindow, text="Description", bg="white").grid(column=1, row=6, pady=20, padx=20)
        description = Text(newProjectWindow, height=5, width=30, borderwidth=5)
        description.grid(column=2, row=6)
        submitBtn = Button(newProjectWindow, text="Submit", bg="white", command=submitNewProject)
        submitBtn.grid(column=2, row=10)

        return

    def uploadProjectHelper(self):
        self.enableDropDown = True
        self.uploadProject()

    def uploadProject(self):
        existingProjectWindow = Toplevel()

        # Initialize window
        existingProjectWindow.title("Projects")
        existingProjectWindow.geometry("300x300")
        existingProjectWindow.configure(background="white")
        existingProjectWindow.resizable(False, False)

        # Add upload frame
        uploadFrame = LabelFrame(existingProjectWindow, text="Begin Upload", bg="white", padx=50, pady=30)
        uploadFrame.pack()

        # Separate for uploading to existing project
        if (self.enableDropDown):

            # variable label for drop down
            existingProjects = StringVar()
            existingProjects.set("Select Existing Project")

            auth = self.odm_API.authenticate()

            obj = self.odm_API.get_list_of_projects(auth)
            projects = []

            for project in obj['results']:
                projects.append(project['name'])

            # Create drop down menu
            dropDown = OptionMenu(uploadFrame, existingProjects, *projects)
            dropDown.grid(column=0, row=1)
            dummyLabel1 = Label(uploadFrame, bd=1, bg="white")
            dummyLabel1.grid(column=0, row=4)

            print('Existing project: ' + existingProjects.get())

            # Disable widget
            self.enableDropDown = False

        # Add buttons and padding for upload frame
        newBtn = Button(uploadFrame, text="Select Folder", width=21, command=self.loadFile)
        newBtn.grid(column=0, row=7)
        dummyLabel2 = Label(uploadFrame, bd=1, bg="white")
        dummyLabel2.grid(column=0, row=10)
        submitBtn = Button(uploadFrame, text="Submit", width=21, command=self.loadWebODM)
        submitBtn.grid(column=0, row=13)

        return

    def loadFile(self):
        file_name = filedialog.askdirectory(initialdir="./")

        if file_name:
            self.list_dir = file_name
            self.pathLabel = Label(self.uploadFrame, text=file_name)
            self.pathLabel.grid(column=0, row=3)

        else:
            messagebox.showinfo("ERROR", "Invalid file directory, try again!")
            raise ValueError("Invalid file directory")

        return self.list_dir

    def loadWebODM(self):
        auth = self.odm_API.authenticate()

        if self.project_name == "":
            return messagebox.showinfo("ERROR", "Project name not properly set")

        if not auth:
            # handle lack of authentication
            return

        self.odm_API.load_images(self.list_dir)

        # get project id for current project
        obj = self.odm_API.get_list_of_projects(auth)
        project_id = ""

        for project in obj['results']:
            if project['name'] == self.project_name:
                project_id = project['id']

        # stitch images
        task_id = self.odm_API.stitch_images(project_id, auth)

        # get progress
        if task_id:
            print('Task id' + task_id)
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
