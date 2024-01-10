# coding:utf-8
"""
    一些小工具(无需单例化)放在这里
"""
import zipfile
import os
from pathlib import Path


def unzip(file: os.PathLike | str, out: os.PathLike | str) -> list[str]:
    """
        解压压缩文件
    """
    zip_file = zipfile.ZipFile(file)
    for names in zip_file.namelist():
        zip_file.extract(names, out)
    return zip_file.namelist()


def make_dir(path: os.PathLike | str):
    """
        若文件夹不存在, 则创建文件夹
    """
    if path != "" and not os.path.exists(path):
        os.mkdir(path)


def make_dir_to(path: os.PathLike | str):
    """
        创建到达路径的全部文件夹
    """
    parts = Path(path).parts
    path = Path()
    for i in parts:
        parts /= i
        make_dir(path)


def make_mc_dir(path: os.PathLike | str):
    """
        创建初始mc文件夹
    """
    path = Path(path)
    make_dir_to(path)
    make_dir_to(path / "versions")
