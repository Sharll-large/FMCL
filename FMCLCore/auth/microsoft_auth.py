# coding:utf-8
"""
    Microsoft账号登陆
"""
import json
import urllib.request
import urllib.parse

# Consts
default_headers = {"Accept": "*/*",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Content-Type": "application/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/103.0.0.0 Safari/537.36 "
                   }


# Post
def post(url, data, headers):
    """
        使用urllib进行post操作
        :param url: 目标url
        :param data: Post Data
        :param headers: Post Headers
        :return: 返回结果
    """
    tmp = urllib.request.Request(url=url, data=urllib.parse.urlencode(data).encode(), headers=headers)
    return urllib.request.urlopen(tmp).read().decode()


# Microsoft Auth
def auth(use_callback: bool, code: str = None):
    """
        进行Microsoft登陆
        :param use_callback: 使用的是否为回调url
        :param code: 注册的回调url
        :return:
    """
    account = {}
    # authcode
    if use_callback:
        authcode = code[code.find("?code=") + 6:code.find("&lc=")]
        ms_data = urllib.parse.urlencode(
            {"client_id": "00000000402b5328", "code": authcode, "grant_type": "authorization_code",
             "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
             "scope": "service::user.auth.xboxlive.com::MBI_SSL"
             }).encode()
    else:
        authcode = code
        ms_data = urllib.parse.urlencode(
            {"client_id": "00000000402b5328", "refresh_token": authcode, "grant_type": "refresh_token",
             "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
             "scope": "service::user.auth.xboxlive.com::MBI_SSL"
             }).encode()

    # 获取用户信息
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = urllib.request.Request(url="https://login.live.com/oauth20_token.srf", data=ms_data, headers=headers)
    tokens = json.loads(urllib.request.urlopen(res).read().decode())

    account["MS_refresh_token"] = tokens["refresh_token"]

    # 刷新token
    data = json.dumps({"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com",
                                      "RpsTicket": tokens["access_token"]
                                      }, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"
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
