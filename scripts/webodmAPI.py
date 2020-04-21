import os
import json
import requests


class WebODMAPI:

    def __init__(self, username='teshobt18', password='deer', PROJECT_ID=3,
                     PROJECT_NAME="deer_project",  ORTHO_RESOLUTION=24,
                     TASK_ID = None, URL='http://localhost:8000'):

        #auth
        self.username = username
        self.password = password

        self.PROJECT_ID = PROJECT_ID #use this to add modify tasks in the Neuvoo project
        self.Task
        self.PROJECT_NAME = PROJECT_NAME # Use this to modify the current project
        self.ORTHO_RESOLUTION = ORTHO_RESOLUTION
        self.URL = 'http://localhost:8000'
        

        self.token = ""
        self.thermal_images  = []
        self.regular_images = []
      

    def authenticate(self)

        try:
            request  = requests.post(URL + '/api/token-auth/', 
                            data={'username': self.username,
                                'password': self.password}).json()
        except:
            print("Unable to authenticate")

        if request:
            self.token =  request['token']


    def load_images(self, file_name):

        source = 'Thermal' # change directory name here according to relative directory needed 
            
        dirs = os.listdir(file_name)

        regular_images = []
        thermal_images = []
        
        
        # images = [
        #     ('images', ('image1.jpg', open('images/DJI_0177.jpg', 'rb'), 'image/jpg')), 
        #     ('images', ('image2.jpg', open('images/DJI_0175.jpg', 'rb'), 'image/jpg')),
        # ]
        for index, file in enumerate(dirs):
            file_path = 'images/{}'.format(file)
            data_file = ('images{}.jpg'.format(index), (file, open(file_path, 'rb'), 'image/jpg'))
            if file.split('.')[-2][-1] == 'R':
                self.thermal_images.append(data_file)
            else:
                self.regular_images.append(data_file)

        return regular_images


    def create_new_project(self, project_name):   
        # Use this to create a new peoject
        res = requests.post('{}/api/projects/'.format(URL), 
                            headers={'Authorization': 'JWT {}'.format(token)},
                            data={'name': project_name}).json()
        project_id = res['id']

        #set project id to that project
        self.PROJECT_ID = project_id


    def stitch_images(self, thermal=True)

       # add a thermal_images task 
        #set up image resolution 
        options = json.dumps([
            {'name': "orthophoto-resolution", 'value': self.}
        ])

        if thermal:
            images = self.thermal_images
        else:
            images = 

        res = requests.post(URL + '/api/projects/{}/tasks/'.format(self.PROJECT_ID), 
                    headers={'Authorization': 'JWT {}'.format(token)},
                    files=images,
                    data={
                        'options': options
                    }
                  ).json()

        self.task_id = res['id']

        return self.task_id

    def get_stitch_status(self):

        while True:
            res = requests.get(URL +  '/api/projects/{}/tasks/{}/'.format(self.PROJECT, self.T 
                        headers={'Authorization': 'JWT {}'.format(token)}).json()

            if res['status'] == status_codes.COMPLETED:
                print("Task has completed!")
                break
            elif res['status'] == status_codes.FAILED:
                print("Task failed: {}".format(res))
                sys.exit(1)
            else:
                print("Processing, hold on...")
                time.sleep(3)




# print(res)
# # task_id = res['id']
# print(task_id)


