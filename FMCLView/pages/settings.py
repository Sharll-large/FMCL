# coding:utf-8
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tk_extend
from tk_extend.framework import GUI
import FMCLCore.System.CoreConfigIO as config
import FMCLView.pages.parts.head as head_part
import FMCLView.i18n

i = FMCLView.i18n.langs
# image=pixel, compound="center" <- 用像素为单位设置label大小的方法(不能用在button上!!!)
pixel = tk.PhotoImage("pixel", width=1, height=1)


def account_settings(_base: tk.Frame) -> tk.Frame:
    def new_ms_account():
        pass

    def new_offline_account():
        name = messagebox.askquestion("First Minecraft Launcher", "请输入账号名:")

    def del_account():
        select = account_list.curselection()[0]
        if select is not None:
            if messagebox.askokcancel("First Minecraft Launcher",
                                      "你确定要删除账号{}吗?".format(config.get("accounts")[select]["name"])):
                accounts = config.get("accounts")
                accounts.pop(select)
                config.change_config_and_safe("accounts", accounts)
                account_list.delete(select)

    base = tk.Frame(_base, width=340, background="#E3F3EE")
    account_list = tk.Listbox(base, width=20, font=("微软雅黑 Light", 10))
    for account in config.get("accounts"):
        account_list.insert(tk.END, "[{}] {}".format(account["type"], account["name"]))
    account_list.grid(column=0, row=0, rowspan=3, padx=(0, 10))
    tk.Button(base, width=30, height=1, text="新建微软账号",
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2").grid(column=1, row=0)
    tk.Button(base, width=30, height=1, text="新建离线账号",
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=new_offline_account
              ).grid(column=1, row=1)
    tk.Button(base, width=30, height=1, text="删除所选账号",
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=del_account).grid(column=1, row=2)

    return base


def page(root: GUI) -> tk.Frame:
    base = tk.Frame(root, width=640, height=360, background="#E3F3EE")
    # 上部
    head_part.get_head_part(base, root, 2).pack(pady=(0, 40))
    # 内容
    now_page = "account"
    content_part = tk.Frame(base, width=640, height=220, background="#E3F3EE")

    first_menu = tk.Listbox(content_part, width=16, foreground="#595959", background="#E3F3EE",
                            activestyle="none", selectforeground="#595959", selectbackground="#BCE2D6", bd=0,
                            highlightthickness=0, selectborderwidth=0, exportselection=False, font=("微软雅黑", 10),
                            justify="right")
    first_menu.insert(tk.END, "账号  ")
    first_menu.select_set(0)
    second_menu = account_settings(content_part)

    first_menu.pack(side="left")
    ttk.Style().configure("grey.TSeparator", background="#595959")
    ttk.Separator(content_part, orient="vertical", style="grey.TSeparator").pack(side="left", fill="y", expand=True,
                                                                                 padx=(0, 10))
    second_menu.pack(side="right", fill="y", expand=True)

    content_part.pack(padx=(60, 60))
    return base
