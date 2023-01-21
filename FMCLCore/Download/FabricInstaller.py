import os
import urllib.request
import json
import subprocess

class FabricInstaller:
    def __init__(self):
        self.versions = None
        self.installer = None

    def refresh(self):
        buf = []
        for i in json.loads(urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/game").read().decode()):
            buf.append(i["version"])
        self.versions = buf
        self.installer = json.loads(urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/installer").read().decode())[0]

    def fabric_versions(self, mc_version):
        if mc_version in self.versions:
            buf = []
            for i in json.loads(urllib.request.urlopen("https://meta.fabricmc.net/v2/versions/loader/" + mc_version).read().decode()):
                buf.append(i["loader"]["version"])
            return buf
        else:
            return []

    def install(self, java, mcpath, mc_version, fabric_version):
        open(os.path.join(mcpath, "fabricinstaller.jar"), "wb+").write(urllib.request.urlopen(self.installer["url"], timeout=5).read())
        subprocess.run([java, "-jar", os.path.join(mcpath, "fabricinstaller.jar"), "client", "-dir", mcpath,
                        "-mcversion", mc_version, "-loader", fabric_version])

a = FabricInstaller()
a.refresh()
print(a.fabric_versions("1.16.5"))
a.install("java", r"C:\Users\Sharll\Desktop\HMCL\.minecraft", "1.16.5", "0.14.1")


