# coding:utf-8
"""
    和launch页面的交互
"""
import FMCLCore.system.CoreConfigIO as config
import FMCLCore.launch.launcher as launcher
import FMCLCore.download.minecraft_patcher as patcher
from FMCLView.i18n import langs
from tkinter import messagebox
import logging
import subprocess
from threading import Thread


# Launch Game
def launch_game(account_id: int, version: str) -> None:
    """
        启动游戏
        :param account_id: 选择的账号编号
        :param version: 选择的版本名
        :return: 无
    """
    if account_id and version and version != langs["Launch.GUI.Choose_Version_Comb.Default"]:
        account = config.get("accounts")[account_id - 1]
        args_1 = {
            "game_directory": config.get(".mc"),
            "version_name": version,
            "java_path": config.get("java"),
            "account": account,
            "java_ram": config.get("ram"),
            "use_jvm_for_performance": config.get("boost"),
            "standalone": config.get("alone"),
        }
        args_2 = {
            "game_directory": config.get(".mc"),
            "version_name": version,
            "threads": config.get("threads"),
            "download_source": config.get("source")
        }
        patcher.patch(**args_2)
        command = launcher.launch(**args_1)
        if command:
            if messagebox.askokcancel("First Minecraft Launcher", langs["Launch.Ask.Launch_Game"].format(version)):
                messagebox.showinfo("First Minecraft Launcher", langs["Launch.Tips.Wait"])
                logging.info("Launch game by command: {}".format(command[0]))

                def _game():
                    accounts = config.get("accounts")
                    accounts[account_id - 1] = command[1]
                    config.change_config_and_safe("accounts", accounts)
                    res = subprocess.getstatusoutput(command[0])
                    import os
                    print("--- Game Stopped --")
                    print(os.getcwd())
                    print(res[0], type(res[0]))
                    if res[0]:
                        logging.error("Game exited unexpectedly(Code {}) with log:\n".format(res[0], res[1]))
                        messagebox.showerror("First Minecraft Launcher",
                                             langs["Launch.Tips.Error"].format(res[0], res[1]))

                Thread(target=_game).start()
        else:
            messagebox.showerror("First Minecraft Launcher", langs["Launch.Tips.NativeError"])
    else:
        messagebox.showerror("First Minecraft Launcher", langs["Launch.Tips.NullError"])
