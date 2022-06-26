from enum import Enum
from typing import Optional


class Level(Enum):
    FATAL = 1
    ERROR = 2
    INFO = 3


class Signal:
    def __init__(
        self,
        message=None,
        level: Optional[Level] = None,
        exception: Optional[Exception] = None,
        context=None,
    ):
        self.message = message
        self.context = context
        if level:
            self.level = level
        elif exception:
            self.level = Level.ERROR
        else:
            self.level = Level.INFO
        self.exception = exception

    def __str__(self):
        message = self.message if self.message else ""
        if self.exception:
            message += f"({type(self.exception)}) {self.exception}"
        if self.context:
            message += f" : {self.context}"
        return f"{self.level} : {message}"
