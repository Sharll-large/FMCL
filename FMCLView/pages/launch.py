# coding:utf-8
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tk_extend.framework import GUI
import FMCLCore.System.CoreConfigIO as config
import FMCLCore.System.CoreVersionGet as versions
import FMCLCore.Launch.CoreLaunchTaskSub as launcher
import FMCLView.pages.parts.head as head_part
import FMCLView.i18n
import subprocess
import logging
from threading import Thread

i = FMCLView.i18n.langs
# image=pixel, compound="center" <- 用像素为单位设置label大小的方法(不能用在button上!!!)
pixel = tk.PhotoImage("pixel", width=1, height=1)


def page(root: GUI) -> tk.Frame:
    base = tk.Frame(root, width=640, height=360, background="#E3F3EE")
    # 上部
    head_part.get_head_part(base, root, 0).pack(pady=(0, 40))
    # 内容
    content_part = tk.Frame(base, width=640, height=220, background="#E3F3EE")
    # TODO: 做头像显示
    headshot = tk.Label(content_part, width=60, height=60, text="头像", image=pixel, compound="center",
                        font=("微软雅黑 Light", 15))

    def callback():
        print("Under develop")

    def refresh_account_list():
        accounts = [i["Launch.GUI.Choose_Account_Comb.Default"]]
        choose_account_comb["values"] = []
        for account in config.get("accounts"):
            accounts.append("[{}] {}".format(account["type"], account["name"]))
        choose_account_comb["values"] = accounts

    def refresh_version_list():
        choose_version_comb["values"] = [i["Launch.GUI.Choose_Version_Comb.Default"]] + versions.local_version(
            config.get(".mc"))

    def launch_game():
        account = choose_account_comb.current()
        version = choose_version_comb.get()
        if account and version and version != i["Launch.GUI.Choose_Version_Comb.Default"]:
            account = config.get("accounts")[account - 1]
            args = {
                "game_directory": config.get(".mc"),
                "version_name": version,
                "java": config.get("java"),
                "playername": account["name"],
                "JvmMaxMemory": config.get("ram"),
                "FixMaxThread": config.get("threads"),
                "UseJvmForPerformance": config.get("boost"),
                "standalone": config.get("alone"),
                "download_source": config.get("source")
            }
            if account["type"] == "microsoft":
                # 微软账号
                args["UUID"] = account["uuid"]
                args["TOKEN"] = account["token"]
            command = launcher.launch(**args)
            if command:
                if messagebox.askokcancel("First Minecraft Launcher", i["Launch.Tips.Ask"].format(version)):
                    messagebox.showinfo("First Minecraft Launcher", i["Launch.Tips.Wait"])
                    logging.info("Launch game by command: {}".format(command))

                    def _game():
                        res = subprocess.getstatusoutput(command)
                        print(res[0], type(res[0]))
                        if res[0]:
                            messagebox.showerror("First Minecraft Launcher",
                                                 i["Launch.Tips.Error"].format(res[0], res[1]))

                    Thread(target=_game).start()
            else:
                messagebox.showerror("First Minecraft Launcher", i["Launch.Tips.NativeError"])
        else:
            messagebox.showerror("First Minecraft Launcher", i["Launch.Tips.NullError"])

    choose_account_comb = ttk.Combobox(content_part, width=20, values=[i["Launch.GUI.Choose_Account_Comb.Default"]],
                                       foreground="#595959", font=("微软雅黑 Light", 10), state="readonly",
                                       postcommand=refresh_account_list)
    choose_account_comb.current(0)

    new_account_btn = tk.Button(content_part, width=22, height=1, text=i["Launch.GUI.New_Account_Btn"],
                                foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
                                compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=callback)

    choose_version_comb = ttk.Combobox(content_part, width=20, values=[i["Launch.GUI.Choose_Version_Comb.Default"]],
                                       foreground="#595959", font=("微软雅黑 Light", 10), state="readonly",
                                       postcommand=refresh_version_list)
    choose_version_comb.current(0)
    version_list_btn = tk.Button(content_part, width=22, height=1, text=i["Launch.GUI.Version_List_Btn"],
                                 foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
                                 compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=callback)
    version_settings_btn = tk.Button(content_part, width=22, height=1, text=i["Launch.GUI.Version_Settings_Btn"],
                                     foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
                                     compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=callback)
    launch_btn = tk.Button(content_part, width=22, height=1, text=i["Launch.GUI.Launch_Btn"], foreground="#595959",
                           background="#BCE2D6", activebackground="#7FC7B1", compound="center", font=("微软雅黑", 8),
                           bd=0, cursor="hand2", command=launch_game)

    headshot.place(x=150, y=0)
    choose_account_comb.place(x=100, y=80)
    new_account_btn.place(x=100, y=110)
    choose_version_comb.place(x=380, y=0)
    version_list_btn.place(x=380, y=80)
    version_settings_btn.place(x=380, y=110)
    launch_btn.place(x=240, y=160)

    content_part.pack()
    return base
