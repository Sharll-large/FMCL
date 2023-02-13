# coding:utf-8
import tkinter as tk
import logging


# 基于tk的单窗口ui框架
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.pages: dict[str, tk.Widget] = {}
        self.now_show: tk.Widget | None = None
        self.switching = False
        super().__init__(*args, **kwargs)

    def page(self, name: str, page: tk.Widget) -> None:
        self.pages[name] = page

    def page_func(self, name):
        return lambda p_func: self.page(name, p_func(self))

    def show_page(self, name):
        if self.pages[name] == self.now_show:
            return
        if self.switching:
            logging.warning("Switch page when switch animation playing")
            return

        def _show():
            before_show = self.now_show
            self.now_show = self.pages[name]
            if before_show:
                self.switching = True
                # 获取窗口大小
                before_show.pack_forget()
                self.now_show.pack()
                self.geometry(self.winfo_geometry())
                # 动画
                before_show.place(x=0, y=0)
                self.now_show.place(x=self.winfo_width(), y=0)

                def animation(now_x: int, target_x: int, speed: float):
                    if abs(target_x - now_x) < 1:
                        before_show.place_forget()
                        self.now_show.place_forget()
                        self.now_show.pack()
                        self.switching = False
                    else:
                        now_x += max(target_x - now_x, 15) * speed
                        before_show.place_configure(x=-now_x)
                        self.now_show.place_configure(x=target_x - now_x)
                        self.after(5, lambda *_: animation(now_x, target_x, speed))

                self.after(1, lambda *_: animation(0, self.winfo_width(), 0.03))
            else:
                self.now_show.pack()

        self.after(0, _show)
