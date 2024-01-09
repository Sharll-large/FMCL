# coding:utf-8
"""
    配置
"""
import json
import logging
import atexit
from pathlib import Path
from typing import Any

import core.system.make_folder

__all__ = ["Config", "config", "read", "write", "change_config", "change_config_and_safe", "get", "fix_depend"]
DEFAULT_CONFIGS = {
    ".mc": str(Path(".minecraft").absolute()),  # mc文件夹
    "java": "java",  # java路径
    "ram": 1024,  # 内存(mb)
    "threads": 80,  # 下载并发数
    "language": "English(US)",  # 语言
    "source": "Default",  # 下载源
    "alone": False,  # 版本隔离
    "boost": False,  # 是否使用jvm优化参数
    "account": [],  # 账号
    "current_account": None,
    "current_version": None,
    "auto_update": False
}


class Config(object):
    """
        用于定获取和更改配置
    """

    def __init__(self, config_path: str = ".first.mcl.json"):
        self.config_path = str(Path(config_path).resolve())
        self.configs = {}

    def read(self) -> dict:
        """
            从文件中读取配置
        """
        with open(self.config_path, "r", encoding="utf-8") as f:
            configs = json.loads(f.read())
        self.configs = configs
        return configs

    def _write_json(self, configs: dict):
        """
            将指定json写入文件
        """
        with open(self.config_path, "w+") as f:
            f.write(json.dumps(configs))

    def write(self, **kwargs):
        """
            将配置写入文件
        """
        logging.info("Saved config to file {}.".format(self.config_path))
        for (key, value) in kwargs.items():
            self.change_config(key, value)
        self._write_json(self.configs)

    def change_config(self, name: str, value: Any) -> None:
        """
            更改配置项
        """
        logging.info("Changed config {} from {} to {}.".format(name, (
            self.configs[name] if name in self.configs.keys() else "None"), value))
        self.configs[name] = value

    def change_config_and_safe(self, name, value):
        """
            更改配置项并保存
        """
        self.change_config(name, value)
        self.write()

    def complete_configs(self) -> None:
        """
            补全配置
        """
        for (key, value) in DEFAULT_CONFIGS:
            if key not in self.configs:
                self.configs[key] = value
                logging.info("Completed item {} with {}".format(key, value))

    def get(self, name):
        """
            获取配置项
        """
        return self.configs[name]

    def fix_depend(self):
        """
            修复配置文件
        """
        if not Path(self.config_path).is_file():
            self.complete_configs()
            self.write()
            logging.info("Config file not found. Create {}.".format(self.config_path))
        else:
            try:
                self.read()
                self.complete_configs()
            except json.decoder.JSONDecodeError:
                logging.info("Config file is broken, fixing.")
                self.complete_configs()
                self.write()
                logging.info("Successfully fixed config.json.")

        core.system.make_folder.make_mc_dir(self.get(".mc"))


config = Config(".first.mcl.json")
config.fix_depend()
config.read()
atexit.register(config.write)
read = config.read
write = config.write
change_config = config.change_config
change_config_and_safe = config.change_config_and_safe
get = config.get
fix_depend = config.fix_depend
