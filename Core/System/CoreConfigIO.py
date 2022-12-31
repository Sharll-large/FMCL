import json
import os
from multiprocessing import cpu_count
import Core.System.Logging
import Core.System.CoreMakeFolderTask

config = os.path.abspath("config.json")


def read():
    return json.load(open(config, "r+"))


def write(playername: str = "player", dotmc: str = ".minecraft", java: str = "java", ram: str = "1024M",
          threads: int = cpu_count() * 8):
    con = {"playername": playername, ".mc": dotmc, "java": java, "ram": ram, "threads": threads}
    writejson(con)


def writejson(all: dict):
    open(config, "w+").write(json.dumps(all))


def fixdepend():
    if not os.path.exists("config.json"):
        write()
        print(Core.System.Logging.showinfo("Config-Checker:\tConfig.json not found. Create config.json."))
    else:
        try:
            read()

        except json.decoder.JSONDecodeError:
            print(Core.System.Logging.showwarning("config.json is broken, fixing."))
            write()
            print(Core.System.Logging.showsuccess("Successfully fixed config.json."))

        finally:
            fixed = False
            config_json = Core.System.CoreConfigIO.read()
            std = {"playername": "player", ".mc": ".minecraft", "java": "java", "ram": "1024M", "threads": 128}
            for i in std:
                if i not in config_json:
                    print(Core.System.Logging.showwarning("Config-Checker:\tMissing object: " + i))
                    config_json[i] = std[i]
                    Core.System.CoreConfigIO.writejson(config_json)
                    fixed = True
            if fixed:
                print(Core.System.Logging.showsuccess("Config-Checker:\tSuccessfully fixed config.json!"))

    Core.System.CoreMakeFolderTask.make_mc_dir(Core.System.CoreConfigIO.read()[".mc"])
