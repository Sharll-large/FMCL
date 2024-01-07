# coding:utf-8
import os
import zipapp

import i18n


def search_all_programs(__path=None):
    programs = list()
    if __path:
        if os.path.isfile(__path):
            if os.path.splitext(__path)[1] == ".py":
                programs.append(__path)
        else:
            for i in os.listdir(__path):
                programs += search_all_programs(os.path.join(__path, i))
    else:
        for i in os.listdir():
            if i not in ["package.py", ".FMCL_Package_Time", "i18n.py"]:
                programs += search_all_programs(i)
    return programs


if __name__ == '__main__':
    os.chdir("../")
    print("FMCL 打包脚本 1.0")

    print("1 转换 i18n.py")
    i18n.main("i18n.xlsx", "FMCLView/i18n.py")

    print("2 过滤冗余的非 Python 文件")
    p = search_all_programs()

    print("3 复制需要的文件")
    for i in p:
        os.makedirs(os.path.dirname(os.path.join(".FMCL_Package_Time", i)), exist_ok=True)
        open(os.path.join(".FMCL_Package_Time", i), "wb").write(open(i, "rb").read())

    print("3 生成Zip-app")
    zipapp.create_archive(".FMCL_Package_Time", "FMCL.pyzw", "/usr/bin/env python3", compressed=True)
