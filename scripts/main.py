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

        # project name and id
        self.project_name = ""
        self.project_id = ""
        self.existingProjects = StringVar()

        # Adding RI logo to window
        self.RI_img = ImageTk.PhotoImage(Image.open(os.path.join(directory, 'images', 'RI_Logo.jpg')))
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
        self.addTask = Button(self.initFrame, text="Add New Task To Existing Project", pady=10, width=30,
                              command=self.uploadProjectHelper)
        self.addTask.grid(column=0, row=7)
        self.dummyLabel2 = Label(self.initFrame, bd=1, bg="white")
        self.dummyLabel2.grid(column=0, row=10)
        self.webBtn = Button(self.initFrame, text="WebODM Settings", pady=10, width=30)
        self.webBtn.grid(column=0, row=13)
        self.dummyLabel3 = Label(self.initFrame, bd=1, bg="white")
        self.dummyLabel3.grid(column=0, row=16)
        self.viewStitchBtn = Button(self.initFrame, text="View Stitched Image", pady=10, width=15, state=DISABLED)
        self.viewStitchBtn.grid(column=0, row=19)

    def createNewProject(self):

        def submitNewProject():
            project_name = name.get("1.0", END)

            # create new project
            auth = self.odm_API.authenticate()

            try:
                self.odm_API.create_new_project(project_name, auth)
            except:
                messagebox.showinfo("Error", "Unable to create a new project. Please try again")
            else:
                messagebox.showinfo("Success", "Created new project: " + project_name)
                self.project_name = project_name
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

    def uploadProjectHelper(self):
        self.enableDropDown = True
        self.uploadProject()

    def uploadProject(self):
        projectsWindow = Toplevel()

        def destroyProjectsWindow():
            projectsWindow.destroy()
            self.loadWebODM()

        # Initialize window
        projectsWindow.title("Projects")
        projectsWindow.geometry("300x300")
        projectsWindow.configure(background="white")
        projectsWindow.resizable(False, False)

        # Add upload frame
        uploadFrame = LabelFrame(projectsWindow, text="Begin Upload", bg="white", padx=50, pady=30)
        uploadFrame.pack()

        # Separate for uploading to existing project
        if (self.enableDropDown):

            # variable label for drop down
            self.existingProjects.set("Select Existing Project")

            auth = self.odm_API.authenticate()

            obj = self.odm_API.get_list_of_projects(auth)
            projects = []

            for project in obj['results']:
                projects.append(project['name'])

            # Create drop down menu
            dropDown = OptionMenu(uploadFrame, self.existingProjects, *projects)
            dropDown.grid(column=0, row=1)
            dummyLabel1 = Label(uploadFrame, bd=1, bg="white")
            dummyLabel1.grid(column=0, row=4)

        # Add buttons and padding for upload frame
        newBtn = Button(uploadFrame, text="Select Folder", width=21, command=self.loadFile)
        newBtn.grid(column=0, row=7)
        dummyLabel2 = Label(uploadFrame, bd=1, bg="white")
        dummyLabel2.grid(column=0, row=10)
        submitBtn = Button(uploadFrame, text="Submit", width=21, command=destroyProjectsWindow)
        submitBtn.grid(column=0, row=13)

    def loadFile(self):
        file_name = filedialog.askdirectory(initialdir="./")

        if file_name:
            self.list_dir = file_name
            messagebox.showinfo("Directory", "Selected directory: " + self.list_dir)
        else:
            messagebox.showinfo("Error", "Invalid file directory, try again!")
            raise ValueError("Invalid file directory")

        return self.list_dir

    def loadWebODM(self):
        auth = self.odm_API.authenticate()

        if self.enableDropDown:
            self.project_name = self.existingProjects.get()
            self.enableDropDown = False

        if self.project_name == "":
            return messagebox.showinfo("ERROR", "Project name not properly set")

        if not auth:
            # handle lack of authentication
            return

        self.odm_API.load_images(self.list_dir)

        # get project id for current project
        obj = self.odm_API.get_list_of_projects(auth)

        # ISSUE -- not getting project ID
        for project in obj['results']:
            if project['name'] == self.project_name:
                print("It worked")
                self.project_id = project['id']

        # stitch images
        print(self.project_name)
        print(self.project_id)
        task_id = self.odm_API.stitch_images(self.project_id, auth)

        # get progress
        if task_id:
            self.get_status(task_id)

        self.odm_API.download_tif(task_id)

    # FIX -- status message here
    def get_status(self, task_id):
        statusWindow = Toplevel()

        statusWindow.title("Status Window")
        statusWindow.geometry("300x300")
        statusWindow.configure(background="white")
        statusWindow.resizable(False, False)

        frame = LabelFrame(statusWindow, bg="white", padx=50, pady=30)
        frame.pack()

        text = Text(frame, width=21)
        btn = Button(frame, text="Finish", width=21)
        btn.grid(column=0, row=7)

        while True:
            text.delete(1.0, END)
            res = self.odm_API.get_stitch_status(task_id)
            if res['status'] == status_codes["COMPLETED"]:
                print("Task has completed!")
                text.insert(END, "Task has completed!")
                break
            elif res['status'] == status_codes["FAILED"]:
                print("Task failed: {}".format(res))
                text.insert(END, "Task failed: {}".format(res))
                sys.exit(1)
            elif res['status'] == status_codes["QUEUED"]:
                print("Task has been qeued")
                text.insert(END, "Task has been qeued")
                time.sleep(3)
            else:
                print("Processing, hold on...")
                text.insert(END, "Processing, hold on...")
                time.sleep(3)
            self.update_idletasks()


if __name__ == "__main__":
    deer_process = DeerVision()
    deer_process.mainloop()
