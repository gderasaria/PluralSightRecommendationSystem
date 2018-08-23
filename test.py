import http.client
import json
import base64
import ssl
# from sklearn.metrics import f1_score
from collections import defaultdict
import numpy as np
import sys
from glob import glob


def UserInfo():
    file_list = glob("data/*.json")
    
    for list_file_index, list_file in enumerate(file_list):
        # icdjson = json.dumps(icd_example)

        print(list_file_index)

        with open(list_file, "r") as json_file:
            user_json = json.load(json_file)

        user_json = json.dumps(user_json)
        
        headers = {'Authorization': 'Basic %s' % base64.b64encode("Gderasaria:12345".encode("ascii")).decode("utf-8"),
                "Content-Type": "application/json"}

        conn = http.client.HTTPSConnection("127.0.0.1:5000", context=ssl._create_unverified_context())

        # Post method for passing data 
        print(user_json)
        r1 = conn.request("post", "api/v1.0/recommend", headers=headers, body=user_json) # this body will carry the data

        # This line will fetch the result back in the json format
        r2 = conn.getresponse()

        print(r2)
        q = r2.read().decode("utf-8")
        print(q)
        # This docs variable will be used for display
        docs = json.loads(q)
        print(docs)

if __name__ == "__main__":

    UserInfo()


