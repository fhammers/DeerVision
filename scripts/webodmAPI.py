import os
import json
import requests

PROJECT_ID = 3 #use this to add modify tasks in the Neuvoo project
PROJECT_NAME = "API_Project" # Use this to modify the current project
ORTHO_RESOLUTION = 24
URL = 'http://localhost:8000'

request  = requests.post(URL + '/api/token-auth/', 
                    data={'username': 'deer',
                          'password': 'welovedeer'}).json()
token = request['token']
print(token)


source = 'Thermal' # change directory name here according to relative directory needed 

    
dirs = os.listdir(source)

images = []
regular_images = []

# for file in dirs:
#     file_path = 'images/{}'.format(file)
#     data_file = ('images', (file, open(file_path, 'rb'), 'image/jpg'))
#     if file.split('.')[-2][-1] == 'R':
#         images.append(data_file)
#     else:
#         regular_images.append(data_file)

# images = [
#     ('images', ('image1.jpg', open('images/DJI_0177.jpg', 'rb'), 'image/jpg')), 
#     ('images', ('image2.jpg', open('images/DJI_0175.jpg', 'rb'), 'image/jpg')),
# ]


       
# Use this to create a new peoject
res = requests.post('{}/api/projects/'.format(URL), 
                    headers={'Authorization': 'JWT {}'.format(token)},
                    data={'name': 'Hello WebODM!'}).json()
project_id = res['id']

# add a thermal_images task 


#set up image resolution 
options = json.dumps([
    {'name': "orthophoto-resolution", 'value': 24}
])


print(images)

# res = requests.post(URL + '/api/projects/{}/tasks/'.format(PROJECT_ID), 
#             headers={'Authorization': 'JWT {}'.format(token)},
#             files=images,
#           ).json()


# print(res)
# # task_id = res['id']
# print(task_id)


