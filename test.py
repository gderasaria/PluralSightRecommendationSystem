import http.client
import json
import base64
import ssl
import numpy as np
import sys
from glob import glob

def UserInfo():
    file_list = glob("models/data/*.json")
    
    for list_file_index, list_file in enumerate(file_list):
        

        with open(list_file, "r") as json_file:
            user_json = json.load(json_file)
        
        user_json = json.dumps(user_json)
        #print(user_json)
        headers = {'Authorization': 'Basic %s' % base64.b64encode("Gderasaria:12345".encode("ascii")).decode("utf-8"),
                "Content-Type": "application/json"}

        conn = http.client.HTTPSConnection("127.0.0.1:5000", context=ssl._create_unverified_context())

        # Post method for passing data 
        r1 = conn.request("post", "api/v1.0/recommend", headers=headers, body=user_json) # this body will carry the data

        # This line will fetch the result back in the json format
        r2 = conn.getresponse()

        q = r2.read().decode("utf-8")
        json_obj = json.loads(q)

        with open('models/results/result.json', 'w') as outfile:
            json.dump(json_obj,outfile)

if __name__ == "__main__":

    UserInfo()


