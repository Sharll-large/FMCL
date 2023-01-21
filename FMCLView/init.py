from FMCLView.tk_extend.dialogs import DefaultStyle


def init_style():
    DefaultStyle.default_root_args = {"background": "#E3F3EE"}
    DefaultStyle.default_label_args = {"foreground": "#595959", "background": "#E3F3EE", "font": ("微软雅黑 Light", 10)}
    DefaultStyle.default_button_args = {"foreground": "#595959", "background": "#BCE2D6", "activebackground": "#7FC7B1",
                                        "font": ("微软雅黑", 8), "bd": 0, "cursor": "hand2"}
    DefaultStyle.default_entry_args = {"foreground": "#595959", "exportselection": False, "font": ("微软雅黑 Light", 8),
                                       "bd": 0}
