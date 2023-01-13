import json
import webbrowser
import urllib.request
import urllib.parse

webbrowser.open("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")

authcode = input("请输入回调链接：")

authcode = authcode[authcode.find("?code=")+6:authcode.find("&lc")]

data = urllib.parse.urlencode({
    "client_id": "00000000402b5328",
    "code": authcode,
    "grant_type": "authorization_code",
    "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
    "scope": "service::user.auth.xboxlive.com::MBI_SSL"
}).encode()

headers = {"Content-Type": "application/json", "Accept": "application/json"}

tokens = json.loads(urllib.request.urlopen(url="https://login.live.com/oauth20_token.srf", data=data, ).read().decode())

data = urllib.parse.urlencode({
    "Properties": {
        "AuthMethod": "RPS",
        "SiteName": "user.auth.xboxlive.com",
        "RpsTicket": "d="+tokens["access_token"]
    },
    "RelyingParty": "<nowiki>http://auth.xboxlive.com</nowiki>",
    "TokenType": "JWT"
}).encode()

print(data)
#print("https://user.auth.xboxlive.com/user/authenticate?" + data.decode())
xbox = json.loads(urllib.request.urlopen(url="https://user.auth.xboxlive.com/user/authenticate", data=data).read().decode())

print(tokens)
print(xbox)
input()


