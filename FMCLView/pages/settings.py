# coding:utf-8
"""
    GUI的Settings部分
"""
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import FMCLCore.system.CoreConfigIO as config
from FMCLCore.active.settings_page import new_ms_account as _new_ms_account
from FMCLCore.active.settings_page import new_offline_account as _new_offline_account
from FMCLView.i18n import langs
import FMCLView.pages.parts.head as head_part
from FMCLView.tk_extend.frame import GUI
from FMCLView.tk_extend.slide_button import SlideButton
import FMCLView.styles as s


def launch_settings(_base: tk.Frame) -> tk.Frame:
    """
        启动设置页面
        :param _base: 父框架
        :return: 启动设置Frame
    """

    def browse_mc_dir() -> None:
        """
            让用户浏览.minecraft文件夹路径
            :return: 无
        """
        mc_dir = filedialog.askdirectory()
        if mc_dir:
            config.change_config_and_safe(".mc", mc_dir)
            path_entry.delete(0, tk.END)
            path_entry.insert(0, mc_dir)
            messagebox.showinfo("First Minecraft Launcher", langs["Settings.Launch.Tips.ChangeSuccess"])
        else:
            messagebox.showinfo("First Minecraft Launcher", langs["Settings.Launch.Tips.PathError"])

    def save() -> None:
        """
            保存.minecraft文件夹设置
            :return: 无
        """
        mc_dir = path_entry.get()
        if mc_dir:
            config.change_config_and_safe(".mc", mc_dir)
            path_entry.delete(0, tk.END)
            path_entry.insert(0, mc_dir)
            messagebox.showinfo("First Minecraft Launcher", langs["Settings.Launch.Tips.ChangeSuccess"])
        else:
            messagebox.showinfo("First Minecraft Launcher", langs["Settings.Launch.Tips.PathError"])

    base = tk.Frame(_base, width=340, background="#E3F3EE")
    # 设置项目的名称
    tk.Label(base, text=langs["Settings.Launch.GUI.McPath"], font=("微软雅黑 Light", 10),
             **s.label()).grid(column=0, row=0, padx=(0, 10), pady=(0, 5))
    tk.Label(base, text=langs["Settings.Launch.GUI.Standalone"], font=("微软雅黑 Light", 10),
             **s.label()).grid(column=0, row=2, padx=(0, 10), pady=(0, 5))
    tk.Label(base, text=langs["Settings.Launch.GUI.Boost"], font=("微软雅黑 Light", 10),
             **s.label()).grid(column=0, row=3, padx=(0, 10), pady=(0, 5))
    # .minecraft路径输入框
    path_entry = tk.Entry(base, width=28, **s.entry())
    path_entry.insert(tk.END, config.get(".mc"))
    path_entry.grid(column=1, row=0, columnspan=2, pady=(0, 5))
    # .minecraft路径选择和保存
    tk.Button(base, width=80, height=20, text=langs["Settings.Launch.GUI.Browse_Btn"], command=browse_mc_dir,
              **s.button()).grid(column=1, row=1, pady=(0, 5), padx=(0, 15), sticky="e")
    tk.Button(base, width=80, height=20, text=langs["Settings.Launch.GUI.Save_Btn"], command=save,
              **s.button()).grid(column=2, row=1, pady=(0, 5), padx=(15, 0), sticky="w")
    # 切换版本隔离和优化函数
    SlideButton(base, width=50, state=(tk.ACTIVE if config.get("alone") else tk.NORMAL),
                onclick=lambda b: config.change_config_and_safe("alone", b.state == tk.ACTIVE)).grid(
        column=1, row=2, pady=(0, 5), sticky="w")
    SlideButton(base, width=50, state=(tk.ACTIVE if config.get("boost") else tk.NORMAL),
                onclick=lambda b: config.change_config_and_safe("boost", b.state == tk.ACTIVE)).grid(
        column=1, row=3, pady=(0, 5), sticky="w")
    return base


def lang_settings(_base: tk.Frame) -> tk.Frame:
    """
        语言设置页面
        :param _base: 父框架
        :return: 语言设置Frame
    """

    def set_lang(_=None) -> None:
        """
            设置语言
            :param _: 无
            :return: 无
        """
        config.change_config_and_safe("language", langs_comb.get())
        langs.lang = langs_comb.get()
        messagebox.showinfo("First Minecraft Launcher", langs["Settings.Lang.Tips.Restart"])

    base = tk.Frame(_base, width=340, background="#E3F3EE")
    langs_comb = ttk.Combobox(base, width=40, values=langs.get_langs(), foreground="#595959", font=("微软雅黑 Light", 10),
                              state="readonly")
    langs_comb.bind("<<ComboboxSelected>>", set_lang)
    langs_comb.current(langs.get_langs().index(config.get("language")))
    langs_comb.pack()
    return base


def account_settings(_base: tk.Frame) -> tk.Frame:
    """
        账号设置页面
        :param _base: 父框架
        :return: 账号设置Frame
    """

    def new_ms_account() -> None:
        """
            创建Microsoft账号
            :return: 无
        """
        result = _new_ms_account()
        if result:
            account_list.insert(tk.END, result)

    def new_offline_account() -> None:
        """
            创建离线账号
            :return: 无
        """
        result = _new_offline_account()
        if result:
            account_list.insert(tk.END, result)

    def del_account() -> None:
        """
            删除所选账号
            :return: 无
        """
        select = account_list.curselection()[0]
        if select is not None:
            if messagebox.askokcancel("First Minecraft Launcher",
                                      langs["Settings.Account.Ask.DeleteAccount"].format(
                                          config.get("accounts")[select]["username"]
                                      )):
                accounts = config.get("accounts")
                accounts.pop(select)
                config.change_config_and_safe("accounts", accounts)
                account_list.delete(select)

    base = tk.Frame(_base, width=360, background="#E3F3EE")
    account_list = tk.Listbox(base, width=20, height=9, font=("微软雅黑 Light", 10), bd=0)
    for account in config.get("accounts"):
        account_list.insert(tk.END, "[{}] {}".format(account["type"], account["username"]))
    account_list.grid(column=0, row=0, rowspan=3, padx=(0, 10))
    tk.Button(base, width=30, height=1, text=langs["Settings.Account.GUI.New_Microsoft_Account_Btn"],
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=new_ms_account
              ).grid(column=1, row=0)
    tk.Button(base, width=30, height=1, text=langs["Settings.Account.GUI.New_Offline_Account_Btn"],
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=new_offline_account
              ).grid(column=1, row=1)
    tk.Button(base, width=30, height=1, text=langs["Settings.Account.GUI.Delete_Active_Account_Btn"],
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=del_account).grid(column=1, row=2)

    return base


def page(root: GUI) -> tk.Frame:
    base = tk.Frame(root, width=640, height=360, background="#E3F3EE")
    # 上部
    head_part.get_head_part(base, root, 2).pack(pady=(0, 40))

    # 内容
    content_part = tk.Frame(base, width=640, height=200, background="#E3F3EE")
    pages = [launch_settings(content_part), lang_settings(content_part), account_settings(content_part)]
    # 换页
    now_page_id = tk.IntVar(value=-1)

    def show_page(_=None):
        if now_page_id.get() != -1:
            pages[now_page_id.get()].pack_forget()
            now_page_id.set(first_menu.curselection()[0])
        else:
            now_page_id.set(0)
        pages[now_page_id.get()].pack(side="left", fill="both")
        pass

    # 一级菜单
    first_menu = tk.Listbox(content_part, width=16, foreground="#595959", background="#E3F3EE",
                            activestyle="none", selectforeground="#595959", selectbackground="#BCE2D6", bd=0,
                            highlightthickness=0, selectborderwidth=0, exportselection=False, font=("微软雅黑", 10),
                            justify="right")
    first_menu.insert(tk.END, langs["Settings.Menu.Launch"] + "  ")
    first_menu.insert(tk.END, langs["Settings.Menu.Lang"] + "  ")
    first_menu.insert(tk.END, langs["Settings.Menu.Account"] + "  ")
    first_menu.select_set(0)
    first_menu.bind("<<ListboxSelect>>", show_page)

    # 分割线
    first_menu.pack(side="left")
    ttk.Separator(content_part, orient="vertical").pack(side="left", padx=(0, 20), fill="y")

    show_page()

    content_part.pack(padx=60, pady=(0, 20), fill="x")
    return base
