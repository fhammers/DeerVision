# {Pytho}
import os
import json
import requests

# {tkinter}
from tkinter import messagebox


class WebODMAPI:
    def __init__(self, username='deer', password='deer', ORTHO_RESOLUTION=24, URL="http://34.69.218.234:8000"):
        # auth
        self.username = username
        self.password = password
        self.URL = URL
        self.token = ""

        # project details
        self.project_id = ""
        self.project_name = ""
        self.ORTHO_RESOLUTION = ORTHO_RESOLUTION

        # images
        self.thermal_images = []
        self.regular_images = []

    def authenticate(self):
        request = ''
        try:
            request = requests.post(self.URL + '/api/token-auth/',
                                    data={'username': self.username,
                                          'password': self.password}).json()

        except:
            print("Unable to authenticate")
            return -1

        finally:
            self.token = request['token']
            return self.token

    def valid_image_file(self, file_path, filename):
        if os.path.isdir(file_path):
            return False
        try:
            file_name, ext = filename.split(".")
        except ValueError:
            return False

        if not file_name or ext != "JPG":
            return False

        return True

    def load_images(self, file_dir):
        source = 'Thermal'  # change directory name here according to relative directory needed

        files = os.listdir(file_dir)
        regular_images = []
        thermal_images = []

        for index, file in enumerate(files):
            file_path = '{}/{}'.format(file_dir, file)
            if self.valid_image_file(file_path, file):
                data_file = ('images{}.jpg'.format(index + 1), (file, open(file_path, 'rb'), 'image/jpg'))
                file_name, ext = file.split(".")

                image_type = file_name[-1]
                print(data_file)
                if image_type == "R":
                    self.thermal_images.append(data_file)
                else:
                    self.regular_images.append(data_file)
        return regular_images

    def create_new_project(self, project_name, auth_token):
        # Use this to create a new peoject
        response = requests.post('{}/api/projects/'.format(self.URL),
                      headers={'Authorization': 'JWT {}'.format(auth_token)},
                      data={'name': project_name}).json()

        return response['id']
        # project_id = res['id']
        #
        # # set project id to that project
        # self.project_id = project_id

    def stitch_images(self, project_id, auth_token, thermal=True):

        # add a thermal_images task
        # set up image resolution
        options = json.dumps([
            {'name': "orthophoto-resolution", 'value': self.ORTHO_RESOLUTION}
        ])

        if thermal:
            images = self.thermal_images
        else:
            images = self.regular_images

        # POST to create a new task on existing project
        res = requests.post(self.URL + '/api/projects/{}/tasks/'.format(project_id),
                            headers={'Authorization': 'JWT {}'.format(auth_token)},
                            files=images,
                            data={
                                'options': options
                            }).json()

        try:
            self.task_id = res['id']
        except TypeError:
            print("Invalid images")
            return 0

        return self.task_id

    def get_stitch_status(self, project_id, task_id=None):
        print(self.token)
        print(self.URL)
        print(self.token)
        res = requests.get('http://34.69.218.234:8000' + '/api/projects/{}/tasks/{}/'.format(project_id, task_id),  
                headers={'Authorization': 'JWT {}'.format(self.token)}).json()

        return res

    def get_list_of_projects(self, auth):
        try:
            projects = requests.get('http://34.69.218.234:8000' + '/api/projects',
                                    headers={'Authorization': 'JWT {}'.format(auth)},
                                    data={'username': 'deer', 'password': 'deer'}).json()
        except:
            print('Unable to get projects')
            return -1

        return projects

    def get_list_of_tasks(self, project_id):
        try:
            tasks = requests.get('http://34.69.218.234:8000' + '/api/projects/{}/tasks/'.format(project_id),
                                 headers={'Authorization': 'JWT {}'.format(self.token)},
                                 data={'username': 'deer', 'password': 'deer'}).json()
        except:
            print('Unable to get tasks')
            return -1
        return tasks

    def download_tif(self, task_id):
        res = requests.get(
            self.URL + "/api/projects/{}/tasks/{}/download/orthophoto.tif".format(self.project_id, task_id),
            headers={'Authorization': 'JWT {}'.format(self.token)},
            stream=True)
        with open("orthophoto.tif", 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        messagebox.showinfo("Success", "Saved as orthophoto.tif")
        print("Saved ./orthophoto.tif")