import platform
import subprocess


def arch():
    _support = {"AMD64": "x86_64"}
    if platform.machine() in _support:
        return _support[platform.machine()]
    return platform.machine()

def system():
    _support = {"Windows": 'windows', "Linux": "linux", "Darwin": "osx"}
    if platform.system() in _support:
        return _support[platform.system()]
    return platform.system()
