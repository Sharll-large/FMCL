import json
import pathlib
from multiprocessing import cpu_count
import FMCLCore.System.Logging
import FMCLCore.System.CoreMakeFolderTask


class Config(object):
    def __init__(self, config_path=".first.mcl.json"):
        self.config_path = str(pathlib.Path(config_path).resolve())
        self.configs = {}

    def read(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            configs = json.loads(f.read())
        self.configs = configs
        return configs

    def change_config(self, name, value):
        self.configs[name] = value

    def init_configs(self):
        self.change_config("player_name", "player")
        self.change_config(".mc", ".minecraft")
        self.change_config("java", "java")
        self.change_config("ram", "1024M")
        self.change_config("threads", 128)
        self.change_config("language", "English(US)")

    def write(self, **kwargs):
        for key in kwargs.keys():
            self.configs[key] = kwargs[key]
        self.write_json(self.configs)

    def write_json(self, configs: dict):
        with open(self.config_path, "w+") as f:
            f.write(json.dumps(configs))

    def get(self, name):
        return self.configs[name]

    def fix_depend(self):
        if not pathlib.Path(self.config_path).is_file():
            self.init_configs()
            self.write()
            print(FMCLCore.System.Logging.showinfo("Config-Checker:\tConfig file not found. Create config.json."))
        else:
            try:
                self.read()
            except json.decoder.JSONDecodeError:
                print(FMCLCore.System.Logging.showwarning("Config-Checker:\tConfig file is broken, fixing."))
                self.init_configs()
                self.write()
                print(FMCLCore.System.Logging.showsuccess("Config-Checker:\tSuccessfully fixed config.json."))

            finally:
                config_json = FMCLCore.System.CoreConfigIO.read()
                std = {"player_name": "player", ".mc": ".minecraft", "java": "java", "ram": "1024M",
                       "threads": cpu_count() * 8, "language": "English(US)"}
                for i in std:
                    if i not in config_json:
                        print(FMCLCore.System.Logging.showwarning("Config-Checker:\tMissing object: " + i))
                        self.change_config(i, std[i])
                self.write()
                print(FMCLCore.System.Logging.showsuccess("Config-Checker:\tSuccessfully fixed config file"))

        FMCLCore.System.CoreMakeFolderTask.make_mc_dir(FMCLCore.System.CoreConfigIO.read()[".mc"])


config = Config(".first.mcl.json")
read = config.read
change_config = config.change_config
write = config.write
write_json = config.write_json
get = config.get
fix_depend = config.fix_depend
