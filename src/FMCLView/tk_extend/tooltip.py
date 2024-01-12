# coding:utf-8
import tkinter as tk


class ToolTip(object):
    """
        提示语控件
    """

    def __init__(self, widget: tk.Widget, text: str):
        self.widget = widget
        self.tip_window = None
        self.id = None
        self.text = text
        self.x = self.y = 0

        self.widget.bind("<Enter>", lambda _: self.showtip())
        self.widget.bind("<Leave>", lambda _: self.hidetip())

    def showtip(self, text: str = None) -> None:
        """
            显示提示信息
            :param text: 提示信息
            :return: 无
        """
        if text:
            self.text = text
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox()
        x = x + self.widget.winfo_rootx() + 30
        y = y + cy + self.widget.winfo_rooty() + 30
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="white", relief=tk.SOLID, borderwidth=1,
                         font=("微软雅黑 Light", "10"))
        label.pack(side=tk.BOTTOM)

    def hidetip(self) -> None:
        """
            隐藏提示信息
            :return: 无
        """
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
