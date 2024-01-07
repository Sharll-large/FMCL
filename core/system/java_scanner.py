# coding:utf-8
"""
    获取java的版本和位数
"""
import re
import subprocess
from os import PathLike


def get_java_version(java_path: PathLike) -> tuple[list[str], int]:
    """
        获取java的版本和位数
        :param java_path:
        :return:
    """
    result = subprocess.getstatusoutput(subprocess.list2cmdline([java_path, "-version"]))[1]
    print(result)
    j_version = re.search(r"\w version \"(.+?)\"", result).group(1).split(".")
    if j_version[0] == "1":
        j_version = j_version[1:]
    j_bits = re.search(r"(\d+.)-Bit", result).group(1)
    return j_version, j_bits


print(get_java_version("C:\\Program Files (x86)\\Java\\jdk1.8.0_202\\bin\\java.exe"))
