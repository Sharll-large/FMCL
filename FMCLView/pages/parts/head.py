# coding:utf-8
"""
    GUI的头部
"""
import tkinter as tk
import FMCLView.styles as s
from FMCLView.tk_extend.frame import GUI
from FMCLView.i18n import langs


def get_head_part(base: tk.Frame, root: GUI, now_choice: int) -> tk.Frame:
    """
        获取头部Frame
        :param base: 父框架
        :param root: 父窗口
        :param now_choice: 目前选择页面
        :return: 头部Frame
    """
    # 主Frame
    head_part = tk.Frame(base, width=640, height=100, background="#E3F3EE")
    # 标题
    title = tk.Label(head_part, width=240, height=54, text="F  M  C  L", font=("微软雅黑 Light", 30), **s.label())
    # 副标题
    subtitle = tk.Label(head_part, width=240, height=10, text="First Minecraft Launcher", font=("微软雅黑 Light", 10),
                        **s.label())
    # 页面选择按钮
    launch_btn = tk.Button(head_part, width=60, height=(100 if now_choice == 0 else 85), text=langs["Header.GUI.Launch"],
                           font=("微软雅黑 Light", 10), command=lambda: root.show_page("launch"),
                           **s.button("font"))
    versions_btn = tk.Button(head_part, width=60, height=(100 if now_choice == 1 else 85), text=langs["Header.GUI.Download"],
                             font=("微软雅黑 Light", 10),
                             **s.button("font"))
    settings_btn = tk.Button(head_part, width=60, height=(100 if now_choice == 2 else 85), text=langs["Header.GUI.Settings"],
                             font=("微软雅黑 Light", 10), command=lambda: root.show_page("settings"),
                             **s.button("font"))
    else_btn = tk.Button(head_part, width=60, height=(100 if now_choice == 3 else 85), text=langs["Header.GUI.Else"],
                         font=("微软雅黑 Light", 10),
                         **s.button("font"))
    # 显示控件
    title.place(x=40, y=20)
    subtitle.place(x=40, y=74)
    launch_btn.place(x=320, y=0)
    versions_btn.place(x=400, y=0)
    settings_btn.place(x=480, y=0)
    else_btn.place(x=560, y=0)
    return head_part
