import sys


def system():
    os = sys.platform
    if os == "win32":
        return "windows"
    elif os == "linux":
        return "linux"
    elif os == "darwin":
        return "osx"
    else:
        return "unknown"
