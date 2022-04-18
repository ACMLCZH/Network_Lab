import requests
import json

url = "http://10.2.110.35:7788"
data = {"OK!": "Yes!"}
res = requests.post(url=url, data=json.dumps(data))

print(res.text)