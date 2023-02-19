# coding:utf-8
"""
    Microsoft账号登陆
"""
import json
import urllib.parse
import urllib.request
import urllib.error

from FMCLCore.auth.microsoft_auth import auth

# Consts
default_headers = {"Accept": "*/*",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Content-Type": "application/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/103.0.0.0 Safari/537.36 "
                   }

class o_auth:
    def __init__(self):
        self.device = None
        self.stream = None
        self.tokens = None
        self.client_id = "69324f03-7b0c-48a3-a995-584127fba992"
        self.scope = "XboxLive.signin offline_access",

    def user_login(self):

        self.device = json.loads(urllib.request.urlopen(urllib.request.Request(
            "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode",
            data=urllib.parse.urlencode({
                "client_id": "69324f03-7b0c-48a3-a995-584127fba992",
                "scope": "XboxLive.signin offline_access"
            }).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"})).read())

        self.stream = urllib.request.Request(
            "https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
            data=urllib.parse.urlencode({
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": "69324f03-7b0c-48a3-a995-584127fba992",
                "code": self.device["device_code"]
            }).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        return self.device["verification_uri"], self.device["user_code"]

    def refresh(self):
        try:
            self.tokens = json.loads(urllib.request.urlopen(self.stream).read())
            return True
        except urllib.error.HTTPError:
            return False


    def xbox_live_auth(self):    pass

    # Microsoft Auth
    def auth(self):
        """
            进行Microsoft登陆
            :param use_callback: 使用的是否为回调url
            :param code: 注册的回调url
            :return:
        """
        account = {"type": "Microsoft", "MS_refresh_token": self.tokens["refresh_token"]}

        print(self.tokens)

        # 刷新token
        data = json.dumps({
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d="+ self.tokens["access_token"]
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }).encode()

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        res = urllib.request.Request(url="https://user.auth.xboxlive.com/user/authenticate", data=data, headers=headers)
        xbox = json.loads(urllib.request.urlopen(res).read().decode())

        data = json.dumps({
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    xbox["Token"]
                ]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }).encode()

        res = urllib.request.Request(url="https://xsts.auth.xboxlive.com/xsts/authorize", data=data)
        xsts = json.loads(urllib.request.urlopen(res).read().decode())

        data = json.dumps({
            "identityToken": f"XBL3.0 x=" + xbox["DisplayClaims"]["xui"][0]["uhs"] + ";" + xsts["Token"]
        }).encode()
        res = urllib.request.Request(url="https://api.minecraftservices.com/authentication/login_with_xbox", data=data,
                                     headers=default_headers)
        mc_token = json.loads(urllib.request.urlopen(res).read().decode())

        account["access_token"] = mc_token["access_token"]

        # 获取账号名和uuid
        default_headers["Authorization"] = "Bearer " + account["access_token"]
        res = urllib.request.Request(url="https://api.minecraftservices.com/minecraft/profile", headers=default_headers)
        del default_headers["Authorization"]
        mcinfo = json.loads(urllib.request.urlopen(res).read().decode())
        account["username"] = mcinfo["name"]
        account["uuid"] = mcinfo["id"]

        return account


a = o_auth()
print(a.user_login())
while True:
    if a.refresh():
        break

print(auth(False, a.auth()["MS_refresh_token"]))
