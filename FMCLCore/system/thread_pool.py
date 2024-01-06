import logging
from concurrent.futures import ThreadPoolExecutor

from FMCLCore.system.CoreConfigIO import config

pool = ThreadPoolExecutor(max_workers=config.get("threads"))

logging.info("Created threadpool, size=" + str(config.get("threads")))
