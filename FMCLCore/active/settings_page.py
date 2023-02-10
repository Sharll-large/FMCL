# coding:utf-8
"""
    和settings页面的交互
"""
import FMCLCore.auth.microsoft_auth as ms_auth
import FMCLCore.auth.offline_auth as of_auth
import FMCLCore.system.CoreConfigIO as config
from FMCLView.tk_extend.dialogs import entry_box
from FMCLView.i18n import langs
from tkinter import messagebox
import webbrowser as wbb
from urllib.error import URLError, HTTPError, ContentTooShortError
import traceback


# Create Microsoft Account
def new_ms_account() -> str | None:
    """
        创建Microsoft账号
        :return: 账号名(创建失败则为None)
    """
    if messagebox.askyesno("First Minecraft Launcher", langs["Settings.Account.Tips.AddMicrosoftAccount"]):
        wbb.open("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code"
                 "&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live"
                 ".com%2Foauth20_desktop.srf")
        url = entry_box(langs["Settings.Account.Ask.Url"], "First Minecraft Launcher", ["URL"])
        messagebox.showinfo("First Minecraft Launcher", langs["Settings.Account.Tips.Wait"])
        if url and url[0]:
            url = url[0]
            try:
                account = ms_auth.auth(True, url)
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
        else:
            messagebox.showerror("First Minecraft Launcher", langs["Settings.Account.Tips.URLError"])


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
