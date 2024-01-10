# coding:utf-8
"""
    GUI的Launch部分
"""
# 框架
import tkinter as tk
import tkinter.ttk as ttk

import FMCLView.pages.parts.head as head_part
import FMCLView.styles as s
import core.local.config as config
import core.local.mc_version as versions
# i18n
from FMCLView.i18n import langs
# 工具
from FMCLView.tk_extend.frame import GUI
from FMCLView.tk_extend.image_transition import cut, resize
from FMCLView.tk_extend.tooltip import ToolTip
from core.active.launche_page import launch_game as _launch_game
from core.auth.ms_account_skin import get_skin_of


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
    # 头像
    avatar_img = tk.PhotoImage()
    avatar = tk.Label(content_part, width=60, height=60, image=avatar_img, font=("微软雅黑 Light", 15),
                      **s.label("background", "image"))
    # 鼠标放的头像上的提示语
    ToolTip(avatar, langs["Settings.Launch.Tips.RefreshAvatar"])

    def callback(*_):
        print("Under develop")

    def refresh_account_list(*_):
        accounts = [langs["Launch.GUI.Choose_Account_Comb.Default"]]
        choose_account_comb["values"] = []
        for account in config.get("accounts"):
            accounts.append("[{}] {}".format(account["type"], account["username"]))
        choose_account_comb["values"] = accounts

    def refresh_version_list(*_):
        choose_version_comb["values"] = [langs["Launch.GUI.Choose_Version_Comb.Default"]] + versions.local_version(
            config.get(".mc"))

    def launch_game(*_):
        _launch_game(choose_account_comb.current(), choose_version_comb.get())

    def save_choosing_account():
        account_id = choose_account_comb.current()
        if account_id:
            config.change_config_and_safe("current_account", account_id)

    def save_choosing_version(*_):
        version_id = choose_version_comb.current()
        if version_id:
            config.change_config_and_safe("current_version", version_id)

    def show_skin(*_):
        account_id = choose_account_comb.current()
        if account_id == 0:
            # 未选择
            avatar_img.blank()
            return
        account = config.get("accounts")[account_id - 1]
        if account["type"] == "Microsoft":
            # 已选择且是微软账户
            _avatar_image = tk.PhotoImage(data=get_skin_of(account["username"], account["uuid"]))
            cut(_avatar_image, avatar_img, 8, 8, 16, 16)
            resize(avatar_img, avatar_img, 8, 8, 60, 60)
            return
        # 已选择且不是微软账户
        avatar_img.blank()

    def refresh_skin(*_):
        account_id = choose_account_comb.current()
        if account_id == 0:
            # 未选择
            avatar_img.blank()
            return
        account = config.get("accounts")[account_id - 1]
        if account["type"] == "Microsoft":
            # 已选择且是微软账户
            _avatar_image = tk.PhotoImage(data=get_skin_of(account["username"], account["uuid"], True))
            cut(_avatar_image, avatar_img, 8, 8, 16, 16)
            resize(avatar_img, avatar_img, 8, 8, 60, 60)
            return
        # 已选择且不是微软账户
        avatar_img.blank()

    avatar.bind("<Button-1>", refresh_skin)

    # 账号部分
    choose_account_comb = ttk.Combobox(content_part, width=20, values=[langs["Launch.GUI.Choose_Account_Comb.Default"]],
                                       postcommand=refresh_account_list, **s.combobox())
    choose_account_comb.bind("<<ComboboxSelected>>", lambda _: show_skin() or save_choosing_account())
    refresh_account_list()
    choose_account_comb.current(config.get("current_account") or 0)
    show_skin()

    new_account_btn = tk.Button(content_part, width=160, height=20, text=langs["Launch.GUI.New_Account_Btn"],
                                command=callback, **s.button())
    # 版本部分
    choose_version_comb = ttk.Combobox(content_part, width=20, values=[langs["Launch.GUI.Choose_Version_Comb.Default"]],
                                       postcommand=refresh_version_list, **s.combobox())
    choose_version_comb.bind("<<ComboboxSelected>>", save_choosing_version)
    refresh_version_list()
    choose_version_comb.current(config.get("current_version") or 0)
    version_list_btn = tk.Button(content_part, width=160, height=20, text=langs["Launch.GUI.Version_List_Btn"],
                                 command=callback, **s.button())
    version_settings_btn = tk.Button(content_part, width=160, height=20, text=langs["Launch.GUI.Version_Settings_Btn"],
                                     command=callback, **s.button())
    # 启动部分
    launch_btn = tk.Button(content_part, width=160, height=20, text=langs["Launch.GUI.Launch_Btn"], command=launch_game,
                           **s.button())
    # 放置控件
    avatar.place(x=150, y=0)
    choose_account_comb.place(x=100, y=80)
    new_account_btn.place(x=100, y=110)
    choose_version_comb.place(x=380, y=0)
    version_list_btn.place(x=380, y=80)
    version_settings_btn.place(x=380, y=110)
    launch_btn.place(x=240, y=160)

    content_part.pack()

    return base
