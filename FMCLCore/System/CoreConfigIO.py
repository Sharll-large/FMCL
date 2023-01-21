import json
import pathlib
import logging
from multiprocessing import cpu_count
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
        logging.info("Change config {} from {} to {}.".format(name, self.configs[name], value))
        self.configs[name] = value

    def init_configs(self):
        self.change_config(".mc", ".minecraft")  # mc文件夹
        self.change_config("java", "java")  # java路径
        self.change_config("ram", 1024)  # 内存(mb)
        self.change_config("threads", cpu_count() * 8)  # 下载核数
        self.change_config("language", "English(US)")  # 语言
        self.change_config("source", "Default")  # 下载源
        self.change_config("alone", False)  # 版本隔离
        self.change_config("boost", False)  # 是否使用jvm优化参数
        self.change_config("accounts", [])  # 账号

    def write(self, **kwargs):
        logging.info("Save config to file {}.".format(self.config_path))
        for key in kwargs.keys():
            self.change_config(key, kwargs[key])
        self.write_json(self.configs)

    def write_json(self, configs: dict):
        with open(self.config_path, "w+") as f:
            f.write(json.dumps(configs))

    def change_config_and_safe(self, name, value):
        self.change_config(name, value)
        self.write()

    def get(self, name):
        return self.configs[name]

    def fix_depend(self):
        if not pathlib.Path(self.config_path).is_file():
            self.init_configs()
            self.write()
            logging.info("Config file not found. Create {}.".format(self.config_path))
        else:
            try:
                self.read()
            except json.decoder.JSONDecodeError:
                logging.info("Config file is broken, fixing.")
                self.init_configs()
                self.write()
                logging.info("Successfully fixed config.json.")

            finally:
                config_json = self.read()
                std = {".mc": ".minecraft", "java": "java", "ram": 1024, "threads": cpu_count() * 8,
                       "language": "English(US)", "source": "Default", "alone": False, "boost": False, "accounts": []}
                for i in std:
                    if i not in config_json:
                        logging.info("Missing object: {}".format(i))
                        self.change_config(i, std[i])
                self.write()
                logging.info("Successfully fixed config file.")

        FMCLCore.System.CoreMakeFolderTask.make_mc_dir(self.get(".mc"))


config = Config(".first.mcl.json")
config.fix_depend()
config.read()
read = config.read
change_config = config.change_config
write = config.write
write_json = config.write_json
change_config_and_safe = config.change_config_and_safe
get = config.get
fix_depend = config.fix_depend
