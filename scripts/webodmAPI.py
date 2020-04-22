import os
import sys
import json
import requests
import time


class WebODMAPI:

    def __init__(self, username='teshobt18', password='deer', PROJECT_ID=2,
                     PROJECT_NAME="deer_project",  ORTHO_RESOLUTION=24,
                     TASK_ID = None, URL='http://localhost:8000'):

        #auth
        self.username = username
        self.password = password

        self.PROJECT_ID = PROJECT_ID #use this to add modify tasks in the Neuvoo project
        self.PROJECT_NAME = PROJECT_NAME # Use this to modify the current project
        self.ORTHO_RESOLUTION = ORTHO_RESOLUTION
        self.URL = 'http://localhost:8000'
        

        self.token = ""
        self.thermal_images  = []
        self.regular_images = []
      

    def authenticate(self):


        request = ''

        try:
            request  = requests.post(self.URL + '/api/token-auth/', 
                                data={'username': self.username,
                                    'password': self.password}).json()

        except:
            print("Unable to authenticate")
            return -1
        finally:
            self.token =  request['token']
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

        source = 'Thermal' # change directory name here according to relative directory needed 
            
        files = os.listdir(file_dir)
        regular_images = []
        thermal_images = []
        
        
        # images = [
        #     ('images', ('image1.jpg', open('images/DJI_0177.jpg', 'rb'), 'image/jpg')), 
        #     ('images', ('image2.jpg', open('images/DJI_0175.jpg', 'rb'), 'image/jpg')),
        # ]
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


    def create_new_project(self, project_name):   
        # Use this to create a new peoject
        res = requests.post('{}/api/projects/'.format(self.URL), 
                            headers={'Authorization': 'JWT {}'.format(self.token)},
                            data={'name': project_name}).json()
        project_id = res['id']

        #set project id to that project
        self.PROJECT_ID = project_id


    def stitch_images(self, thermal=True):

       # add a thermal_images task 
        #set up image resolution 
        options = json.dumps([
            {'name': "orthophoto-resolution", 'value': self.ORTHO_RESOLUTION}
        ])

        if thermal:
            images = self.thermal_images
        else:
            images = self.regular_images
        print(images, self.PROJECT_ID)
        
        
        res = requests.post(self.URL + '/api/projects/{}/tasks/'.format(self.PROJECT_ID), 
                    headers={'Authorization': 'JWT {}'.format(self.token)},
                    files=images,
                    data={
                        'options': options
                    }
                  ).json()


        try:
            self.task_id = res['id']
        except TypeError:
            print("Invalid images")
            return 0

        return self.task_id

    def get_stitch_status(self, task_id = None):

    
            res = requests.get(self.URL +  '/api/projects/{}/tasks/{}/'.format(self.PROJECT_ID, task_id),
                        headers={'Authorization': 'JWT {}'.format(self.token)}).json()

            return res

           

    def download_tif(self, task_id):
        res = requests.get(self.URL + "/api/projects/{}/tasks/{}/download/orthophoto.tif".format(self.PROJECT_ID, task_id), 
                        headers={'Authorization': 'JWT {}'.format(self.token)},
                        stream=True)
        with open("orthophoto.tif", 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        print("Saved ./orthophoto.tif")




# print(res)
# # task_id = res['id']
# print(task_id)


