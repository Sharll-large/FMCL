import tkinter as tk
import tkinter.ttk
import tkinter.messagebox
import webbrowser
import FMCLCore.Auth.MicrosoftAuth
import FMCLCore.System.CoreConfigIO
import FMCLView.Const
import urllib.error

def main():
    def openlink():
        webbrowser.open("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
    def postauth():
        try:
            temp = FMCLCore.Auth.MicrosoftAuth.Auth(True, callbacklink.get())
            FMCLCore.System.CoreConfigIO.add_account({
                "type": "microsoft",
                "name": temp["username"],
                "uuid": temp["uuid"],
                "token": temp["access_token"]
            })
            tk.messagebox.showinfo("FMCL", FMCLView.Const.get("Account.Success") + temp["username"])
        except urllib.error.URLError or urllib.error.HTTPError or urllib.error.ContentTooShortError as e:
            tk.messagebox.showerror("FMCL", FMCLView.Const.get("Account.Fail") + "\n" + repr(e))

    def showhelp():
        tk.messagebox.showinfo("FMCL", FMCLView.Const.get("Account.HelpText"))

    def addoffline():
        name = offlinename.get()
        offlinename.delete(0, "end")
        FMCLCore.System.CoreConfigIO.add_account({
            "type": "offline",
            "name": name
        })
        tk.messagebox.showinfo("FMCL", FMCLView.Const.get("Account.Success") + name)

    def refresh():
        accounts["values"] = FMCLCore.System.CoreConfigIO.get_account()

    def delete():
        accounts.set("")
        FMCLCore.System.CoreConfigIO.delete_account(accounts.current())


    f = tk.ttk.Frame()
    callbacklink = tk.ttk.Entry(f)
    callbacklink.grid(row=0, column=1)
    tk.ttk.Label(f, text=FMCLView.Const.get("Account.AboutMicrosoft")).grid(row=0, column=0)
    tk.ttk.Button(f, text=FMCLView.Const.get("Account.OpenURL"), command=openlink).grid(row=0, column=2)
    tk.ttk.Button(f, text=FMCLView.Const.get("Account.Auth"), command=postauth).grid(row=0, column=3)

    offlinename = tk.ttk.Entry(f)
    offlinename.grid(row=1, column=1)
    tk.ttk.Label(f, text=FMCLView.Const.get("Account.Offline")).grid(row=1, column=0)
    tk.ttk.Button(f, text=FMCLView.Const.get("Account.Add"), command=addoffline).grid(row=1, column=2)

    tk.ttk.Button(f, text=FMCLView.Const.get("Account.Help"), command=showhelp).grid(row=2, column=0)

    tk.ttk.Label(f, text=FMCLView.Const.get("Account.Have")).grid(row=3, column=0)
    accounts = tk.ttk.Combobox(f, postcommand=refresh, state='readonly')
    accounts.grid(row=3, column=1)
    tk.ttk.Button(f, text=FMCLView.Const.get("Account.Delete"), command=delete).grid(row=3, column=2)

    return f