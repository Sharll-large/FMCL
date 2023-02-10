# coding:utf-8
"""
    GUI的Launch部分
"""
# 框架
import tkinter as tk
import tkinter.ttk as ttk

import FMCLCore.system.CoreConfigIO as config
import FMCLCore.system.CoreVersionGet as versions
import FMCLView.pages.parts.head as head_part
import FMCLView.styles as s
from FMCLCore.active.launche_page import launch_game as _launch_game
# i18n
from FMCLView.i18n import langs as i
# 工具
from FMCLView.tk_extend.frame import GUI


def page(root: GUI) -> tk.Frame:
    """
        获取Launcher Frame
        :param root: 父窗口
        :return: Launcher Frame
    """
    # 主Frame
    base = tk.Frame(root, width=640, height=360, background="#E3F3EE")
    # 头部
    head_part.get_head_part(base, root, 0).pack(pady=(0, 40))
    # 内容
    content_part = tk.Frame(base, width=640, height=220, background="#E3F3EE")
    # TODO: 做头像显示
    headshot = tk.Label(content_part, width=60, height=60, text="头像", font=("微软雅黑 Light", 15),
                        **s.label("background"))

    def callback():
        print("Under develop")

    def refresh_account_list():
        accounts = [i["Launch.GUI.Choose_Account_Comb.Default"]]
        choose_account_comb["values"] = []
        for account in config.get("accounts"):
            accounts.append("[{}] {}".format(
                ("Microsoft" if account.get("MS_refresh_token") else "Offline"),
                account["username"]))
        choose_account_comb["values"] = accounts

    def refresh_version_list():
        choose_version_comb["values"] = [i["Launch.GUI.Choose_Version_Comb.Default"]] + versions.local_version(
            config.get(".mc"))

    def launch_game():
        _launch_game(choose_account_comb.current(), choose_version_comb.get())

    # 账号部分
    choose_account_comb = ttk.Combobox(content_part, width=20, values=[i["Launch.GUI.Choose_Account_Comb.Default"]],
                                       postcommand=refresh_account_list, **s.combobox())
    choose_account_comb.current(0)

    new_account_btn = tk.Button(content_part, width=160, height=20, text=i["Launch.GUI.New_Account_Btn"],
                                command=callback, **s.button())
    # 版本部分
    choose_version_comb = ttk.Combobox(content_part, width=20, values=[i["Launch.GUI.Choose_Version_Comb.Default"]],
                                       postcommand=refresh_version_list, **s.combobox())
    choose_version_comb.current(0)
    version_list_btn = tk.Button(content_part, width=160, height=20, text=i["Launch.GUI.Version_List_Btn"],
                                 command=callback, **s.button())
    version_settings_btn = tk.Button(content_part, width=160, height=20, text=i["Launch.GUI.Version_Settings_Btn"],
                                     command=callback, **s.button())
    # 启动部分
    launch_btn = tk.Button(content_part, width=160, height=20, text=i["Launch.GUI.Launch_Btn"], command=launch_game,
                           **s.button())
    # 放置控件
    headshot.place(x=150, y=0)
    choose_account_comb.place(x=100, y=80)
    new_account_btn.place(x=100, y=110)
    choose_version_comb.place(x=380, y=0)
    version_list_btn.place(x=380, y=80)
    version_settings_btn.place(x=380, y=110)
    launch_btn.place(x=240, y=160)

    content_part.pack()

    return base
