import urllib.request
import json

device = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode?"
    "client_id=69324f03-7b0c-48a3-a995-584127fba992&scope=user.read%20openid%20profile",
    headers={"Content-Type": "application/x-www-form-urlencoded"})).read())

print(device)

print("https://login.microsoftonline.com/consumers/oauth2/v2.0/token?"
      "grant_type=urn:ietf:params:oauth:grant-type:device_code&client_id=69324f03-7b0c-48a3-a995-584127fba992&device_code=" + device["device_code"])

while True:
    input()
    print(urllib.request.urlopen(
        urllib.request.Request("https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
                               data=("grant_type=urn:ietf:params:oauth:grant-type:device_code&client_id=69324f03-7b0c-48a3-a995-584127fba992&device_code=" + device["device_code"]).encode(),
                               headers={"Content-Type": "application/x-www-form-urlencoded"})).read())

