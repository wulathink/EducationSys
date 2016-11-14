import requests
import json

user_info = {'username':'michael', 'password':'123456', 'userNo':'10001','phone':'18583680490'}
headers = {'content-type':'application/json'}
r = requests.post("http://127.0.0.1:8080/register", data=json.dumps(user_info), headers=headers)

print r.json()

json_object = r.json()

print json_object['status']
print json_object['msg']
