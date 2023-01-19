import tkinter as tk
from tk_extend import GUI


def get_head_part(base: tk.Frame, root: GUI, now_choice: int) -> tk.Frame:
    # image=pixel, compound="center" <- 用像素为单位设置label大小的方法(不能用在button上!!!)
    # 上部
    pixel = tk.PhotoImage(width=0, height=0)
    head_part = tk.Frame(base, width=640, height=100, background="#E3F3EE")
    title = tk.Label(head_part, width=240, height=54, text="F  M  C  L", image=pixel, foreground="#595959",
                     background="#E3F3EE", compound="center", font=("微软雅黑 Light", 30))
    subtitle = tk.Label(head_part, width=240, height=10, text="First Minecraft Launcher", image=pixel,
                        foreground="#595959", background="#E3F3EE", compound="center", font=("微软雅黑 Light", 10))
    launch_btn = tk.Button(head_part, width=8, height=(5 if now_choice == 0 else 4), text="Launch\n-\n启动",
                           background="#BCE2D6", activebackground="#7FC7B1", compound="center",
                           font=("微软雅黑 Light", 10), bd=0, command=lambda: root.show_page("launch"))
    versions_btn = tk.Button(head_part, width=8, height=(5 if now_choice == 1 else 4), text="Versions\n-\n版本",
                             background="#BCE2D6", activebackground="#7FC7B1", compound="center",
                             font=("微软雅黑 Light", 10), bd=0)
    settings_btn = tk.Button(head_part, width=8, height=(5 if now_choice == 2 else 4), text="Settings\n-\n设置",
                             background="#BCE2D6", activebackground="#7FC7B1", compound="center",
                             font=("微软雅黑 Light", 10), bd=0, command=lambda: root.show_page("settings"))
    else_btn = tk.Button(head_part, width=8, height=(5 if now_choice == 3 else 4), text="Else\n-\n其它",
                         background="#BCE2D6", activebackground="#7FC7B1", compound="center",
                         font=("微软雅黑 Light", 10), bd=0)
    title.place(x=40, y=20)
    subtitle.place(x=40, y=74)
    launch_btn.place(x=320, y=0)
    versions_btn.place(x=400, y=0)
    settings_btn.place(x=480, y=0)
    else_btn.place(x=560, y=0)
    return head_part
