import requests
import json

# url = "http://10.2.110.35:7788"
url = "http://localhost:7788"
data = open("sample_wifi_data.txt", "r").readline().strip()
print(data)

res = requests.post(url=url, data=data)

print(res.text)