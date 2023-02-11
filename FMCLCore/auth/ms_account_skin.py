# coding:utf-8
"""
    获取玩家皮肤
"""
import base64
import json
import os
import urllib.parse
import urllib.request
import FMCLCore.system.CoreConfigIO as config


def get_skin_of(name: str, uuid: str, refresh: bool = False) -> bytes | None:
    """
        获取玩家皮肤(Microsoft账号限定)
        :param name: 玩家名
        :param uuid: 玩家uuid
        :param refresh: 是否需要重新下载
        :return: 图片内容(png格式)(失败则为None)
    """
    file_path = os.path.join(config.get(".mc"), "assets", "skins", "sk", "skin_" + name)
    if refresh or not os.path.exists(file_path):
        # 皮肤缓存不存在或需要刷新
        try:
            things = json.loads(urllib.request.urlopen(
                urllib.parse.urljoin("https://sessionserver.mojang.com/session/minecraft/profile/", uuid)).read())
        except json.decoder.JSONDecodeError:
            # json解析错误
            return None
        if "errorMessage" in things:
            # 错误
            return None
        for i in things["properties"]:
            if i["name"] == "textures":
                skin_url = json.loads(base64.b64decode(i["value"]).decode())["textures"]["SKIN"]["url"]
                content = urllib.request.urlopen(skin_url).read()
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(content)
                return content
    else:
        # 皮肤缓存存在
        with open(file_path, "rb") as f:
            content = f.read()
        return content
