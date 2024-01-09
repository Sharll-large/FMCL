# coding:utf-8
"""
    获取java的版本和位数
"""
import re
import os
import subprocess
from pathlib import Path
from os import PathLike

from smt.tools.struct import struct

__all__ = ["JavaVersion", "JavaScanner", "java_scanner", "get_java_version", "scan_all"]
JavaVersion = struct(["path", "version", "bits"])
POSSIBLE_JAVA = ["Java", "BellSoft", "AdoptOpenJDK", "Zulu", "Microsoft", "Eclipse Foundation", "Semeru"]


class JavaScanner(object):
    """
        用于获取java的版本和位数
    """

    def __init__(self):
        self.cached_paths = {}

    def get_java_version(self, java_path: PathLike | str) -> JavaVersion:
        """
            获取java的版本和位数
            :param java_path: java路径
            :return: java版本对象(包含path, version和bits)
        """
        java_path = Path(java_path)
        if java_path in self.cached_paths:
            return self.cached_paths[java_path]
        result = subprocess.getstatusoutput(subprocess.list2cmdline([java_path, "-version"]))[1]
        version = re.search(r"\w version \"(.+?)\"", result).group(1).split(".")
        if version[0] == "1":
            version = version[1:]
        bits = re.search(r"(\d+.)-Bit", result).group(1)
        java_version = JavaVersion(java_path, version, bits)
        self.cached_paths[java_path] = java_version
        return java_version

    def scan_all(self) -> dict[Path, JavaVersion]:
        """
            扫描全部java
            :return: 全部java的路径和java版本对象(包含path, version和bits)
        """
        # 环境变量内Java检测
        for i in os.getenv("path").split(";"):
            # path中, 如果文件夹(或/bin文件夹)内包含java.exe, 则说明是java文件夹
            path = Path(i)
            executable_path1 = path / "java.exe"
            executable_path2 = path / "bin" / "java.exe"
            if executable_path1.exists():
                self.get_java_version(executable_path1)
            if executable_path2.exists():
                self.get_java_version(executable_path2)
        # TODO: 文件Java检测
        return self.cached_paths


java_scanner = JavaScanner()
get_java_version = java_scanner.get_java_version
scan_all = java_scanner.scan_all
scan_all()
