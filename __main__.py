# coding:utf-8
# FMCL Boot Entry
"""
    启动FMCL
"""
import logging
import os.path
# ----------
# Authors:
# 底层: sharll, AGJ
# GUI: pxinz
# i18n: AGJ, pxinz
# ----------
# Libraries:
# 框架: tkinter
# ----------
# Thank for using FMCL!
# ----------
import sys
import tkinter.messagebox
import traceback
from os import chdir, path, remove

import FMCLCore.system.CoreConfigIO as config
import FMCLCore.system.thread_pool
import FMCLView.main

__author__ = ["sharll", "AGJ", "pxinz"]


def main(*args) -> None:
    """
        启动程序
        :param args: 启动参数
        :return: 无
    """
    chdir(path.join("/", *path.split(args[0])[:-1]))
    # 配置logger
    logging.basicConfig(
        level=(args[args.index("-log-level") + 1] if "-log-level" in args else logging.DEBUG),
        filename=(args[args.index("-log-file") + 1] if "-log-file" in args else "latest.log"),
        filemode="w",
        format="[%(asctime)s] %(name)s %(threadName)s - %(filename)-8s line %(lineno)d | %(levelname)-9s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # 运行
    logging.info("FMCL started.")
    if os.path.isfile("_update_FMCL.py"):
        remove("_update_FMCL.py")
    if config.get("auto_update"):
        # 热更新
        from threading import Thread
        from update import check
        Thread(target=check, args=[__file__]).start()

    # 开启线程池

    FMCLView.main.main()

    FMCLCore.system.thread_pool.pool.shutdown()  # 关闭线程池

    logging.info("FMCL stopped.")


if __name__ == "__main__":
    try:
        main(*sys.argv)
    except Exception as e:
        error_msg = traceback.format_exc()
        sys.stderr.write(error_msg)
        logging.error(f"Error happened! Error message:\n {error_msg}")
        tkinter.messagebox.showerror("FMCL Error", "Error message:\n" + error_msg)
    except KeyboardInterrupt:
        logging.info("FMCL stopped.")
