# coding:utf-8
import os
import shutil
import zipapp
from pathlib import Path

import i18n


def search_program_files(path: Path, force: bool = False) -> list[Path]:
    if path.is_file():
        if path.suffix in [".py"]:
            return [path]
        return []
    elif path.is_dir():
        if not force and path.name[0] == "." or path.name in ["programming tools", "docs"]:
            return []
        res = []
        for i in os.listdir(path):
            res += search_program_files(path / i)
        return res


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
    i18n.main("./programming tools/i18n.xlsx", "./FMCLView/i18n.py")

    print("2 过滤冗余的非 Python 文件")
    p = search_program_files(Path("./"), True)

    print("3 复制需要的文件")
    if os.path.exists(".FMCL_Package_Time"):
        shutil.rmtree(".FMCL_Package_Time")
    dir_path = Path(".FMCL_Package_Time")
    for i in p:
        os.makedirs(dir_path / i.parent, exist_ok=True)
        shutil.copy2(i, dir_path / i)
        print(f"Copied file {i} -> {dir_path / i}")

    print("3 生成Zip-app")
    zipapp.create_archive(".FMCL_Package_Time", "FMCL.pyzw", "/usr/bin/env python3", compressed=True)
