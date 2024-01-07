# coding:utf-8
import logging
from concurrent.futures import ThreadPoolExecutor

from core.system.config import config

pool = ThreadPoolExecutor(max_workers=config.get("threads"))

logging.info("Created threadpool, size=" + str(config.get("threads")))
