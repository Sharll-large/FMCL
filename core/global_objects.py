# coding:utf-8
"""
    一些全局变量
"""
import logging
from concurrent.futures import ThreadPoolExecutor

from core.system.config import config

__all__ = ["thread_pool"]
# 线程池
thread_pool = ThreadPoolExecutor(max_workers=config.get("threads"))
logging.info("Created threadpool, size=" + str(config.get("threads")))
