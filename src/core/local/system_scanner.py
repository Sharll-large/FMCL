# coding:utf-8
"""
    扫描系统信息
"""
import platform

__all__ = ["SystemScanner", "system_scanner", "scan", "get_arch", "get_system"]
SUPPORTED_ARCHITECTURES = {"AMD64": "x86_64"}
SUPPORTED_SYSTEMS = {"Windows": 'windows', "Linux": "linux", "Darwin": "osx"}


class SystemScanner(object):
    """
        用于获取设备的架构和系统
    """

    def __init__(self):
        self.arch = None
        self.system = None

    def scan(self):
        arch_ = platform.machine()
        system_ = platform.system()
        if arch_ in SUPPORTED_ARCHITECTURES:
            self.arch = SUPPORTED_ARCHITECTURES[arch_]
        else:
            self.arch = arch_
        if system_ in SUPPORTED_SYSTEMS:
            self.system = SUPPORTED_SYSTEMS[system_]
        else:
            self.arch = system_

    def get_arch(self):
        return self.arch

    def get_system(self):
        return self.system


system_scanner = SystemScanner()
system_scanner.scan()
scan = system_scanner.scan
get_arch = system_scanner.get_arch
get_system = system_scanner.get_system
