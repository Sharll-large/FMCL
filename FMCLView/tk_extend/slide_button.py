# coding:utf-8
import tkinter as tk


class SlideButton(tk.Canvas):
    def __init__(self, master=None, width=80, thick=25, background="#E3F3EE", foreground="#BCE2D6"):
        super().__init__(master=master, width=width, height=thick)
        self.state = tk.NORMAL
        self.width = width
        self.thick = thick
        self.bg = background
        self.fg = foreground
        self.draw()
        self.bind("<Button-1>", self.onclick)

    def draw(self, pos=0):
        self.create_line(self.thick / 2, self.thick / 2, self.width - self.thick / 2, self.thick / 2, capstyle="round",
                         fill=self.fg, width=self.thick)
        self.create_line(self.thick / 2, self.thick / 2, self.width - self.thick / 2, self.thick / 2, capstyle="round",
                         fill=self.bg, width=self.thick - 5)
        self.create_line(self.thick / 2 + pos, self.thick / 2, self.thick / 2 + pos, self.thick / 2, capstyle="round",
                         fill=self.fg, width=self.thick - 10)

    def onclick(self, _):
        if self.state == tk.NORMAL:
            self.state = tk.ACTIVE

            def _flush(p):
                return lambda: self.draw(poses[p])

            pos = 0
            poses = []
            max_pos = int(self.width - self.thick)
            while round(pos) != max_pos:
                poses.append(pos)
                pos += (max_pos - pos) * 0.12
            poses.append(max_pos)
            for i in range(len(poses)):
                self.after(i * 20, _flush(i))
            self.draw(max_pos)

        else:
            self.state = tk.NORMAL

            def _flush(p):
                return lambda: self.draw(poses[p])

            pos = int(self.width - self.thick)
            poses = []
            max_pos = 0
            while round(pos) != max_pos:
                poses.append(pos)
                pos += (max_pos - pos) * 0.12
            poses.append(max_pos)
            for i in range(len(poses)):
                self.after(i * 20, _flush(i))
            self.draw(max_pos)
