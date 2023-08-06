"""
Module: 'logging' on micropython-v1.18-win32
"""
# MCU: {'machine': 'unknown', 'sysname': 'unknown', 'platform': 'win32', 'nodename': 'unknown', 'ver': 'v1.18', 'release': '1.18.0', 'name': 'micropython', 'family': 'micropython', 'port': 'win32', 'version': '1.18.0', 'mpy': 517, 'build': ''}
# Stubber: 1.11.2
from typing import Any

CRITICAL = 50 # type: int
INFO = 20 # type: int
DEBUG = 10 # type: int
ERROR = 40 # type: int
WARNING = 30 # type: int
NOTSET = 0 # type: int
def getLogger(*args, **kwargs) -> Any:
    ...

def basicConfig(*args, **kwargs) -> Any:
    ...

def info(*args, **kwargs) -> Any:
    ...

def debug(*args, **kwargs) -> Any:
    ...


class Logger():
    level = 0 # type: int
    def setLevel(self, *args, **kwargs) -> Any:
        ...

    def exception(self, *args, **kwargs) -> Any:
        ...

    def isEnabledFor(self, *args, **kwargs) -> Any:
        ...

    def critical(self, *args, **kwargs) -> Any:
        ...

    def info(self, *args, **kwargs) -> Any:
        ...

    def log(self, *args, **kwargs) -> Any:
        ...

    def warning(self, *args, **kwargs) -> Any:
        ...

    def debug(self, *args, **kwargs) -> Any:
        ...

    def error(self, *args, **kwargs) -> Any:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...

