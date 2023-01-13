import json
import webbrowser
import urllib.request
import urllib.parse


def post(url, data, headers):
    tmp = urllib.request.Request(url=url, data=urllib.parse.urlencode(data).encode(), headers=headers)
    return urllib.request.urlopen(tmp).read().decode()

def Auth(refresh_token: str=None):
    defaultheaders = {"Accept": "*/*",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "zh-CN,zh;q=0.9",
                      "Connection": "keep-alive",
                      "Content-Type": "application/json",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                      }
    informations = {}
    if refresh_token is None:
        webbrowser.open("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
        authcode = input("请输入回调链接：")
        authcode = authcode[authcode.find("?code=")+6:authcode.find("&lc=2052")]
        MSdata = urllib.parse.urlencode({"client_id": "00000000402b5328", "code": authcode, "grant_type": "authorization_code",
                                         "redirect_uri": "https://login.live.com/oauth20_desktop.srf", "scope": "service::user.auth.xboxlive.com::MBI_SSL"
                                         }).encode()
    else:
        authcode = refresh_token
        MSdata = urllib.parse.urlencode({"client_id": "00000000402b5328", "refresh_token": authcode, "grant_type": "refresh_token",
                                         "redirect_uri": "https://login.live.com/oauth20_desktop.srf", "scope": "service::user.auth.xboxlive.com::MBI_SSL"
                                         }).encode()

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = urllib.request.Request(url="https://login.live.com/oauth20_token.srf", data=MSdata, headers=headers)
    tokens = json.loads(urllib.request.urlopen(res).read().decode())

    informations["MS_refresh_token"] = tokens["refresh_token"]

    data = json.dumps({"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com",
                                       "RpsTicket": tokens["access_token"]
        },"RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"
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
                                 headers=defaultheaders)
    mctoken = json.loads(urllib.request.urlopen(res).read().decode())
    informations["access_token"] = mctoken["access_token"]

    headerstmp = defaultheaders
    headerstmp["Authorization"] = "Bearer " + informations["access_token"]
    res = urllib.request.Request(url="https://api.minecraftservices.com/minecraft/profile", headers=headerstmp)
    mcinfo = json.loads(urllib.request.urlopen(res).read().decode())
    informations["username"] = mcinfo["name"]
    informations["uuid"] = mcinfo["id"]

    return informations

print(Auth())
input()