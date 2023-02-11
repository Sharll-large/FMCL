# coding: utf-8
"""
    更新和防篡改
"""
import json
import urllib.request
import urllib.parse
import urllib.error
import hashlib
import FMCLCore.system.CoreConfigIO as config
import os
import tkinter.messagebox

def _get_version():
    update_url = "https://sharll-large.github.io/FMCL/version.json" if config.get("source") == "Default" else None

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}

    req = urllib.request.Request(url=update_url, headers=headers, )
    response = urllib.request.urlopen(req, timeout=5).read()
    version = json.loads(response)
    return version


def check():

    filepath = os.path.dirname(__file__)

    if os.path.isfile(filepath):
        sha_object = hashlib.sha256()
        sha_object.update(open(filepath, "rb").read())
        try:
            version = _get_version()
        except TimeoutError:

            tkinter.messagebox.showwarning("First Minecraft Launcher", "连接到更新服务器超时")
            return

        if sha_object.hexdigest() != version["sha256"]:
            buf = "检测到新的FMCL版本"+version["version"]+"\n"
            for i in version["log"]:
                buf += i + "\n"
            buf += "是否进行更新?"

            tkinter.messagebox.askokcancel("First Minecraft Launcher", buf)

    else:
        tkinter.messagebox.showwarning("First Minecraft Launcher", "您似乎解压了FMCL, 如果你不是开发者，这种做法不被推荐。自动更新已停用！")

_get_version()