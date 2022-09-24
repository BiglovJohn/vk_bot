import os
import logging as log
from os import environ
from logging.handlers import *


if not os.path.exists("log"):
    os.mkdir("log")


class Environment:
    GROUP_ID: str = str(environ.get(
        "GROUP_ID", default="YOUR_GROUP_ID"
    ))

    TOKEN: str = str(environ.get(
        "TOKEN", default="YOUR_TOKEN"
    ))

    API_VERSION: float = float(environ.get(
        "API_VERSION", default="YOUR_API_VERSION"
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
