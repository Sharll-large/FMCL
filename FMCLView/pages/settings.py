# coding:utf-8
import webbrowser as wbb
from urllib.error import URLError, HTTPError, ContentTooShortError
import traceback

import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

import FMCLCore.System.CoreConfigIO as config
import FMCLCore.Auth.MicrosoftAuth as auth
import FMCLView.i18n
import FMCLView.pages.parts.head as head_part
from FMCLView.tk_extend.framework import GUI
from FMCLView.tk_extend.dialogs import entry_box

i = FMCLView.i18n.langs
# image=pixel, compound="center" <- 用像素为单位设置label大小的方法(不能用在button上!!!)
pixel = tk.PhotoImage("pixel", width=1, height=1)


def lang_settings(_base: tk.Frame) -> tk.Frame:
    def set_lang(_=None):
        config.change_config_and_safe("language", langs_comb.get())
        i.lang = langs_comb.get()
        messagebox.showinfo("First Minecraft Launcher", i["Settings.Lang.Tip"])

    base = tk.Frame(_base, width=340, background="#E3F3EE")
    langs_comb = ttk.Combobox(base, width=60, values=i.get_langs(), foreground="#595959", font=("微软雅黑 Light", 10),
                              state="readonly")
    langs_comb.bind("<<ComboboxSelected>>", set_lang)
    langs_comb.current(i.get_langs().index(config.get("language")))
    langs_comb.pack()
    return base


def account_settings(_base: tk.Frame) -> tk.Frame:
    def new_ms_account():
        if messagebox.askyesno("First Minecraft Launcher",
                               "添加一个Microsoft账号的方法:\n"
                               "1. 打开特定链接并进行Microsoft登陆\n"
                               "2. 登陆完毕后会重定向到另一个url, 将url复制过来, FMCL会帮你登陆\n"
                               "点击确定键跳转至链接"):
            wbb.open("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code"
                     "&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live"
                     ".com%2Foauth20_desktop.srf")
            url = entry_box("请输入重定向到的url:", "First Minecraft Launcher", ["URL"])
            messagebox.showinfo("First Minecraft Launcher", "关闭该窗口后进行登陆, 请耐心等待并不要关闭启动器窗口")
            if url and url[0]:
                url = url[0]
                try:
                    account = auth.Auth(True, url)
                    accounts = config.get("accounts")
                    accounts.append({"type": "microsoft",
                                     "name": account["username"],
                                     "uuid": account["uuid"],
                                     "token": account["access_token"]})
                    config.change_config_and_safe("accounts", accounts)
                    account_list.insert(tk.END, "[microsoft] {}".format(account["username"]))
                    messagebox.showinfo("First Minecraft Launcher", i["Settings.Account.AddAccountSuccess"])
                except (URLError, HTTPError, ContentTooShortError):
                    messagebox.showerror("First Minecraft Launcher", i["Settings.Account.NetworkError"])
                except KeyError:
                    messagebox.showerror("First Minecraft Launcher", i["Settings.Account.KeyError"])
                except Exception:
                    err_msg = traceback.format_exc()
                    messagebox.showerror("First Minecraft Launcher", i["Settings.Account.UnknownError"].format(err_msg))
            else:
                messagebox.showerror("First Minecraft Launcher", i["Settings.Account.URLError"])

    def new_offline_account():
        name = entry_box(i["Settings.Account.Ask_AccountName"], "First Minecraft Launcher",
                         i["Settings.Account.Name.AccountName"])
        if name and name[0]:
            name = name[0]
            accounts = config.get("accounts")
            accounts.append({"type": "offline", "name": name})
            config.change_config_and_safe("accounts", accounts)
            account_list.insert(tk.END, "[offline] {}".format(name))
            messagebox.showinfo("First Minecraft Launcher", i["Settings.Account.AddAccountSuccess"])

    def del_account():
        select = account_list.curselection()[0]
        if select is not None:
            if messagebox.askokcancel("First Minecraft Launcher",
                                      i["Settings.Account.Ask_DeleteAccount"].format(
                                          config.get("accounts")[select]["name"]
                                      )):
                accounts = config.get("accounts")
                accounts.pop(select)
                config.change_config_and_safe("accounts", accounts)
                account_list.delete(select)

    base = tk.Frame(_base, width=340, background="#E3F3EE")
    account_list = tk.Listbox(base, width=20, font=("微软雅黑 Light", 10))
    for account in config.get("accounts"):
        account_list.insert(tk.END, "[{}] {}".format(account["type"], account["name"]))
    account_list.grid(column=0, row=0, rowspan=3, padx=(0, 10))
    tk.Button(base, width=30, height=1, text=i["Settings.Account.New_Microsoft_Account_Btn"],
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=new_ms_account
              ).grid(column=1, row=0)
    tk.Button(base, width=30, height=1, text=i["Settings.Account.New_Offline_Account_Btn"],
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=new_offline_account
              ).grid(column=1, row=1)
    tk.Button(base, width=30, height=1, text=i["Settings.Account.Delete_Active_Account_Btn"],
              foreground="#595959", background="#BCE2D6", activebackground="#7FC7B1",
              compound="center", font=("微软雅黑", 8), bd=0, cursor="hand2", command=del_account).grid(column=1, row=2)

    return base


def page(root: GUI) -> tk.Frame:
    base = tk.Frame(root, width=640, height=360, background="#E3F3EE")
    # 上部
    head_part.get_head_part(base, root, 2).pack(pady=(0, 40))

    # 内容

    content_part = tk.Frame(base, width=640, height=220, background="#E3F3EE")
    pages = [lang_settings(content_part), account_settings(content_part)]
    now_page_id = tk.IntVar(value=-1)

    def show_page(_=None):
        if now_page_id.get() != -1:
            pages[now_page_id.get()].pack_forget()
            now_page_id.set(first_menu.curselection()[0])
        else:
            now_page_id.set(0)
        pages[now_page_id.get()].pack(side="left", fill="y", expand=True, padx=(0, 10))

    first_menu = tk.Listbox(content_part, width=16, foreground="#595959", background="#E3F3EE",
                            activestyle="none", selectforeground="#595959", selectbackground="#BCE2D6", bd=0,
                            highlightthickness=0, selectborderwidth=0, exportselection=False, font=("微软雅黑", 10),
                            justify="right")
    first_menu.insert(tk.END, i["Settings.Menu.Lang"] + "  ")
    first_menu.insert(tk.END, i["Settings.Menu.Account"] + "  ")
    first_menu.select_set(0)
    first_menu.bind("<<ListboxSelect>>", show_page)

    first_menu.pack(side="left")
    ttk.Separator(content_part, orient="vertical").pack(side="left", fill="y", expand=True,
                                                        padx=(0, 10))
    show_page()

    content_part.pack(padx=(60, 60))
    return base
