# coding:utf-8
"""
    和settings页面的交互
"""

import time
import traceback
import webbrowser as wbb
from tkinter import messagebox
from urllib.error import URLError, HTTPError, ContentTooShortError

import core.auth.oauth as oa
import core.auth.offline_auth as of_auth
import core.local.config as config
import pyperclip
from FMCLView.i18n import langs
from FMCLView.tk_extend.dialogs import entry_box


# Create Microsoft Account
def new_ms_account() -> str | None:
    """
        创建Microsoft账号
        :return: 账号名(创建失败则为None)
    """
    if messagebox.askyesno("First Minecraft Launcher", langs["Settings.Account.Tips.AddMicrosoftAccount"]):
        things = oa.user_login()
        print(things)

        if things[0] == "https://www.microsoft.com/link":
            # 若返回link为https://www.microsoft.com/link，则可以简化登录过程
            wbb.open(things[0] + "?otc=" + things[1])
        else:
            wbb.open(things[0])
            pyperclip.copy(things[1])

        start = time.time()
        while True:
            a = oa.refresh()
            if a:
                break
            else:
                if time.time() - start > things[2]:
                    messagebox.showinfo("First Minecraft Launcher", langs["Settings.Account.Timeout"])
                    return None
        try:
            account = oa.auth(a)
            accounts = config.get("accounts")
            accounts.append(account)
            config.change_config_and_safe("accounts", accounts)
            messagebox.showinfo("First Minecraft Launcher", langs["Settings.Account.Tips.AddAccountSuccess"])
            return "[Microsoft] {}".format(account["username"])
        except (URLError, HTTPError, ContentTooShortError):
            messagebox.showerror("First Minecraft Launcher", langs["Settings.Account.Tips.NetworkError"])
        except Exception:
            err_msg = traceback.format_exc()
            messagebox.showerror("First Minecraft Launcher",
                                 langs["Settings.Account.Tips.UnknownError"].format(err_msg))


# Create offline account
def new_offline_account() -> str | None:
    name = entry_box(langs["Settings.Account.Ask.AccountName"], "First Minecraft Launcher",
                     langs["Settings.Account.Name.AccountName"])
    if name and name[0]:
        name = name[0]
        accounts = config.get("accounts")
        accounts.append(of_auth.auth(name))
        config.change_config_and_safe("accounts", accounts)
        messagebox.showinfo("First Minecraft Launcher", langs["Settings.Account.Tips.AddAccountSuccess"])
        return "[Offline] {}".format(name)
