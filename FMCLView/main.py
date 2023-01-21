from FMCLView.tk_extend.framework import GUI
from FMCLView.init import init_style


def main():
    gui = GUI()
    from FMCLView.pages import launch, settings
    init_style()
    gui.geometry("640x360")
    gui.title("First Minecraft Launcher")

    gui.page_func("launch")(launch.page)
    gui.page_func("settings")(settings.page)

    gui.show_page("launch")
    gui.mainloop()


if __name__ == '__main__':
    main()
