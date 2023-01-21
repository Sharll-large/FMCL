# FMCL Boot Entry.
import sys
import logging
import FMCLView.main
import tkinter.messagebox
import traceback


def main(*args):
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
    FMCLView.main.main()
    logging.info("FMCL stopped.")


if __name__ == "__main__":
    print(sys.argv)
    try:
        main(sys.argv)
    except Exception as e:
        error_msg = traceback.format_exc()
        logging.error(f"Error happened! Error message:\n {error_msg}")
        tkinter.messagebox.showerror("FMCL Error", "Error message:\n" + error_msg)
    except KeyboardInterrupt:
        logging.info("FMCL stopped.")
