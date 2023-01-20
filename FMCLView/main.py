from FMCLView.tk_extend.framework import GUI
from FMCLView.tk_extend.button_box import ButtonBox


def main():
    ButtonBox.default_root_args = {"background": "#E3F3EE"}
    ButtonBox.default_text_args = {"background": "#E3F3EE", "font": ("微软雅黑 Light", 10)}
    ButtonBox.default_btn_args = {"background": "#BCE2D6", "activebackground": "#7FC7B1",
                                  "font": ("微软雅黑 Light", 10), "bd": 0}
    gui = GUI()
    from FMCLView.pages import launch, settings
    gui.geometry("640x360")
    gui.title("First Minecraft Launcher")

    gui.page_func("launch")(launch.page)
    gui.page_func("settings")(settings.page)

    gui.show_page("launch")
    gui.mainloop()


if __name__ == '__main__':
    main()
