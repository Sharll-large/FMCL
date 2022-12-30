import subprocess
import threading
import tkinter as tk
import tkinter.messagebox


def main(command: list[str]):
    def call():
        print(command)
        result = subprocess.getstatusoutput(command)
        if result[0] != 0:
            tk.messagebox.showerror("Error", "Error throwed while launching, exit code: " + str(result[0]) + "(" + str(hex(result[0])))
            tk.messagebox.showerror("Error", result[1])

    if tk.messagebox.askyesno("Launch", "going to launch game, continue?"):
        threading.Thread(target=call).start()
