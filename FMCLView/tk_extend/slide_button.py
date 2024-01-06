# coding:utf-8
import tkinter as tk


class SlideButton(tk.Canvas):
    def __init__(self, master=None, width=80, thick=25, background="#E3F3EE", foreground="#BCE2D6", state=tk.NORMAL,
                 onclick=None):
        super().__init__(master=master, width=width, height=thick, bd=0)
        self.state = state
        self.width = width
        self.thick = thick
        self.bg = background
        self.fg = foreground
        self.click_func = onclick
        self.animate = False
        if state == tk.ACTIVE:
            self.pos = self.target_pos = width - thick
        else:
            self.pos = self.target_pos = 0
        self.draw()
        self.bind("<Button-1>", self.onclick)

    def draw(self):
        """
            绘制按钮
            :return: 无
        """
        self.delete(tk.ALL)
        # 背景
        self.create_rectangle(0, 0, self.width + 5, self.thick + 5, fill=self.bg)
        # 外部圆角方块
        self.create_line(self.thick / 2, self.thick / 2, self.width - self.thick / 2, self.thick / 2, capstyle="round",
                         fill=self.fg, width=self.thick)
        # 内部圆角方块
        self.create_line(self.thick / 2, self.thick / 2, self.width - self.thick / 2, self.thick / 2, capstyle="round",
                         fill=self.bg, width=self.thick - 5)
        # 滑块
        self.create_line(self.thick / 2 + self.pos, self.thick / 2, self.thick / 2 + self.pos, self.thick / 2,
                         capstyle="round",
                         fill=self.fg, width=self.thick - 10)

    def _flush(self):
        if round(self.pos) == self.target_pos:
            self.pos = self.target_pos
            self.draw()
            self.animate = False
        else:
            self.pos += (self.target_pos - self.pos) * 0.12
            self.draw()
            self.after(20, self._flush)

    def onclick(self, _):
        if self.state == tk.NORMAL:
            self.state = tk.ACTIVE
            self.target_pos = self.width - self.thick
        else:
            self.state = tk.NORMAL
            self.target_pos = 0
        self.draw()
        if not self.animate:
            self.animate = True
            self.after(20, self._flush)
        if self.click_func:
            self.click_func(self)
