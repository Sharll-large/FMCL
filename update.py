# coding:utf-8
# coding: utf-8
"""
    更新和防篡改
"""
import hashlib
import json
import os
import sys
import time
import tkinter.messagebox
import urllib.error
import urllib.parse
import urllib.request

import core.local.config as config
from FMCLView.i18n import langs

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}


def _get_version():
    """
        获取最新版本
        :return:
    """
    update_url = "https://sharll-large.github.io/FMCL/api/latest-version.json" if config.get(
        "source") == "Default" else "https://gitee.com/AGJCreate/test-repo/raw/master/verification.json"

    request = urllib.request.Request(url=update_url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5).read()
    version = json.loads(response)
    return version


def check(file_path: os.PathLike) -> None:
    """
        热更新
        :return: 无
    """
    main_file = os.path.split(file_path)
    update_file = os.path.split(__file__)
    if __file__ == file_path or main_file[:-1] == update_file[:-1] and \
            main_file[-2].split(".")[-1] in ["pyz", "pyzw"] and main_file[-1].split(".")[-1] in ["py", "pyw"]:
        # 检查sha256与版本
        try:
            version = _get_version()
        except TimeoutError:
            return
        sha_object = hashlib.sha256()
        sha_object.update(open(os.path.join("/", *main_file[:-1]), "rb").read())

        if sha_object.hexdigest() != version["sha256"]:
            if tkinter.messagebox.askokcancel("First Minecraft Launcher", langs["Update.Ask.Update"].format(
                    version["version"], "\n".join(["· " + log for log in version["log"]]))):
                with open("_update_FMCL.py", "w") as f:
                    f.write(
                        'import urllib.request,os,sys,time;print("*Updating FMCL*");req=urllib.request.Request('
                        'url=sys.argv[1],headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU '
                        '360SE"});print("Downloading FMCL...");response=urllib.request.urlopen(req,timeout=5);'
                        'print("Writing FMCL to file...");content=response.read(128);f=open("FMCL.pyzw","wb");\n'
                        'while content:f.write(content);content=response.read(128)\nf.close();'
                        'print("*Download successfully, opening FMCL*");os.local("start /B python FMCL.pyzw");'
                        'time.sleep(0.2)'
                    )
                    os.system("start /b python _update_FMCL.py " + version["url"])
                    time.sleep(0.2)
                    sys.exit(0)

    else:
        config.change_config_and_safe("auto_update", False)
        tkinter.messagebox.showwarning("First Minecraft Launcher",
                                       langs["Update.Tips.UnZipWarning"])
