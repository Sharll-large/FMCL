import json
import urllib.request

def get(vertype, download_source: str = "Default", refresh=False):
    if refresh:
        if download_source == "Default": manifest= "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        elif download_source == "BMCLAPI": manifest= "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"
        elif download_source == "MCBBS": manifest= "https://download.mcbbs.net/mc/game/version_manifest_v2.json"
        else: return False
        information = urllib.request.urlopen(manifest).read()
        meta = json.loads(information)
        open(".fmcl.version_meta.json", "wb+").write(information)
    else:
        meta = json.load(open(".fmcl.version_meta.json", "rb+"))

    verlist = []

    lt_release, lt_snapshot = meta["latest"]["release"], meta["latest"]["snapshot"]

    for i in meta["versions"]:
        if i["id"] == lt_release:
            lt_release = i
        if i["id"] == lt_snapshot:
            lt_snapshot = i
        if i["type"] in vertype:
            verlist.append(i)

    return lt_release, lt_snapshot, verlist
