import requests
import json

request_data = {'username':'michael', 'password':'123456'}
headers = {'content-type':'application/json'}
r = requests.post("http://127.0.0.1:8080/login", data=json.dumps(request_data), headers=headers)

json_object = r.json()
print json_object['status']
print json_object['msg']
