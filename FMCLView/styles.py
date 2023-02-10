# coding:utf-8
"""
    GUI页面的样式
"""
import tkinter as tk


class Style(object):
    """
        样式类
    """

    def __init__(self, styles: dict):
        """
            初始化样式类
            :param styles: 样式dict
        """
        self.styles = styles

    def __call__(self, *disabled, **kwargs) -> dict:
        """
            获取样式类中的样式
            :param disabled: 不需要返回的项目
            :param kwargs: 无
            :return: 获取到的样式
        """
        result = {}
        for k, v in self.styles.items():
            if k not in disabled:
                result[k] = v
        return result


frame: Style
label: Style
button: Style
entry: Style
combobox: Style


def init() -> None:
    """
        初始化样式, 做成函数形式是因为PhotoImage和Style均需要主窗口来创建
        :return: 无
    """
    global frame, label, button, entry, combobox
    # pixel: 1*1的像素
    pixel = tk.PhotoImage(width=0, height=0)
    # Frame
    frame = Style({"background": "#E3F3EE"  # Color
                   })
    # Label
    label = Style({"image": pixel, "compound": tk.CENTER,  # Size
                   "foreground": "#595959", "background": "#E3F3EE"  # Color
                   })
    # Button
    button = Style({"image": pixel, "compound": tk.CENTER,  # Size
                    "foreground": "#595959", "background": "#BCE2D6", "activebackground": "#7FC7B1",  # Color
                    "font": ("微软雅黑", 8), "bd": 0,  # Style
                    "cursor": "hand2"  # Active
                    })
    # Entry
    entry = Style({"foreground": "#595959",  # Color
                   "font": ("微软雅黑", 10), "bd": 0,  # Style
                   "exportselection": False  # Active
                   })
    # Combobox
    combobox = Style({"foreground": "#595959",  # Color
                      "font": ("微软雅黑 Light", 10),  # Style
                      "state": "readonly"  # Active
                      })
