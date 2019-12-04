import logging
import os

import planforge

PLANFORGE_LOG = os.environ.get("PLANFORGE_LOG")

logger = logging.getLogger("planforge")


def console_log_level():
    if planforge.log in ["debug", "info"]:
        return planforge.log
    elif PLANFORGE_LOG in ["debug", "info"]:
        return PLANFORGE_LOG
    else:
        return None


def log_debug(message, *args, **kwargs):
    msg = message % args
    logger.debug(msg, **kwargs)
    if console_log_level() == "debug":
        print(msg)


def log_info(message, *args, **kwargs):
    msg = message % args
    logger.info(message, **kwargs)
    if console_log_level() in ["debug", "info"]:
        print(msg)
