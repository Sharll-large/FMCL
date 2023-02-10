import base64
import json
import urllib.parse
import urllib.request


def get_skin_of(uuid: str) -> bytes:
    things = json.loads(urllib.request.urlopen(urllib.parse.urljoin("https://sessionserver.mojang.com/session/minecraft/profile/", uuid)).read())
    if "errorMessage" in things:
        return None
    for i in things["properties"]:
        if i["name"] == "textures":
            return urllib.request.urlopen(json.loads(base64.b64decode(i["value"]).decode())["textures"]["SKIN"]["url"]).read()

