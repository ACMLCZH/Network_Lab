import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--local", action="store_true", default=False)
args = parser.parse_args()

if args.local:
    url = "http://localhost:7788"
else:
    url = "http://10.0.83.13:7788"
    # url = "http://10.129.203.88:7788"
fin = open("sample_wifi_data.txt", "r")

for data in fin:
    data = data.strip()
    print(data)
    res = requests.post(url=url, data=data)
    print(res.text)

fin.close()