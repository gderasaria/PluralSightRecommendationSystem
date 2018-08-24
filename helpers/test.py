# Will contain the code to run the project by passing the userid in json format. 

import requests
import os
from flask import Flask 
import json

print("Enter the user id")
user_id = input()
print(user_id)
params = {
			'user_handle' : user_id,			
		 }
print("object created")
BASE_URL = "http://0.0.0.0:5000"
r = requests.get("{}/summary".format(BASE_URL) , json = json.dumps(params))
print("json_created")
with open('/results/similar_users.json','w') as f:
	f.write(r.text)