import json
import os
from multiprocessing import cpu_count
import FMCLCore.System.Logging
import FMCLCore.System.CoreMakeFolderTask

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
        print(FMCLCore.System.Logging.showinfo("Config-Checker:\tConfig.json not found. Create config.json."))
    else:
        try:
            read()

        except json.decoder.JSONDecodeError:
            print(FMCLCore.System.Logging.showwarning("config.json is broken, fixing."))
            write()
            print(FMCLCore.System.Logging.showsuccess("Successfully fixed config.json."))

        finally:
            fixed = False
            config_json = FMCLCore.System.CoreConfigIO.read()
            std = {"playername": "player", ".mc": ".minecraft", "java": "java", "ram": "1024M", "threads": 128}
            for i in std:
                if i not in config_json:
                    print(FMCLCore.System.Logging.showwarning("Config-Checker:\tMissing object: " + i))
                    config_json[i] = std[i]
                    FMCLCore.System.CoreConfigIO.writejson(config_json)
                    fixed = True
            if fixed:
                print(FMCLCore.System.Logging.showsuccess("Config-Checker:\tSuccessfully fixed config.json!"))

    FMCLCore.System.CoreMakeFolderTask.make_mc_dir(FMCLCore.System.CoreConfigIO.read()[".mc"])
