# coding:utf-8
import tkinter as tk


# 基于tk的单窗口ui框架
class GUI(tk.Tk):
    def __init__(self):
        self.pages = {}
        self.now_show = None
        super().__init__()

    def page(self, name: str, page: tk.Widget) -> None:
        self.pages[name] = page

    def page_func(self, name):
        return lambda p_func: self.page(name, p_func(self))

    def show_page(self, name):
        def _show():
            if self.now_show:
                self.now_show.pack_forget()
            self.pages[name].pack()
            self.now_show = self.pages[name]

        self.after(0, _show)
