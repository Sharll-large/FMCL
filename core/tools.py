# coding:utf-8
"""
    一些小工具(无需单例化)放在这里
"""
import zipfile
from os import PathLike


def unzip(file: PathLike | str, out: PathLike | str) -> list[str]:
    """
        解压压缩文件
    """
    zip_file = zipfile.ZipFile(file)
    for names in zip_file.namelist():
        zip_file.extract(names, out)
    return zip_file.namelist()
