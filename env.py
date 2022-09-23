import os
import logging as log
from os import environ
from logging.handlers import *


if not os.path.exists("log"):
    os.mkdir("log")


class Environment:
    GROUP_ID: str = str(environ.get(
        "GROUP_ID", default="211527491"
    ))

    TOKEN: str = str(environ.get(
        "TOKEN", default="e67872ebfc86d94ebd6ed43d7db7ba925fc3fd7b603699a44fe79a762f1f6b8bdf6f529be8300983a80c9"
    ))

    API_VERSION: float = float(environ.get(
        "API_VERSION", default="5.131"
    ))


log.basicConfig(
    level=log.DEBUG,
    format='[%(asctime)s.%(msecs)03d] [%(levelname)-6s] [%(filename)-24s] : %(message)s',
    handlers=[
        log.StreamHandler(),
        TimedRotatingFileHandler(filename="log/application.log", when="D", backupCount=14)
    ]
)


ENV = Environment()
