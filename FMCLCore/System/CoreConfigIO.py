import json
import os

import FMCLCore.System.CoreMakeFolderTask
import FMCLCore.System.Logging

config = os.path.abspath(".first.mcl.json")
really = {}

def read():
    return json.load(open(config, "r+", encoding="utf-8"))

def writejson(conf: dict):
    open(config, "w+", encoding="utf-8").write(json.dumps(conf))

def add_account(account: dict):
    tmp = read()
    tmp["Accounts"].append(account)
    writejson(tmp)

def delete_account(number: int):
    tmp = read()
    del tmp["Accounts"][number]
    writejson(tmp)

def get_account():
    accountlist = []
    for i in read()["Accounts"]:
        accountlist.append("[" + i["type"] + "] " + i["name"])
    return accountlist

def fixdepend():
    std = {"About": "This file is very important! DO NOT EDIT OR SHARE!", ".mc": ".minecraft", "java": "java", "ram": "1024M", "threads": 64, "Language": "English", "Accounts": []}
    if not os.path.exists(config):
        writejson(std)
        print(FMCLCore.System.Logging.showinfo("Config-Checker:\t" + config + " not found. Create " + config + "."))
    else:
        try:
            read()

        except json.decoder.JSONDecodeError:
            print(FMCLCore.System.Logging.showwarning(config + " is broken, fixing."))
            writejson(std)
            print(FMCLCore.System.Logging.showsuccess("Successfully fixed " + config + "."))

        finally:
            fixed = False
            config_json = FMCLCore.System.CoreConfigIO.read()
            for i in std:
                if i not in config_json:
                    print(FMCLCore.System.Logging.showwarning("Config-Checker:\tMissing object: " + i))
                    config_json[i] = std[i]
                    FMCLCore.System.CoreConfigIO.writejson(config_json)
                    fixed = True
            if fixed:
                print(FMCLCore.System.Logging.showsuccess("Config-Checker:\tSuccessfully fixed " + config + "!"))

    FMCLCore.System.CoreMakeFolderTask.make_mc_dir(FMCLCore.System.CoreConfigIO.read()[".mc"])
