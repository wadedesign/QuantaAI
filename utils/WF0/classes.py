"""A file for all the classes."""
import json
from dataclasses import dataclass

from nextcord.ext import commands

from .errors import print_error

__all__ = (
    "CodeStats",
    "Config",
    "CustomEmojis",
    "Map",
)


@dataclass
class CodeStats:
    """A class to easily manage code statistics"""

    comments: int = 0
    coroutines: int = 0
    characters: int = 0
    functions: int = 0
    classes: int = 0
    lines: int = 0
    strings: int = 0
    filecount: int = 0
    imports: int = 0
    commands: int = 0
    if_: int = 0
    else_: int = 0
    elif_: int = 0
    docstrings: int = 0
    embeds = 0


class Map(dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value


class Config(Map):
    """A class to handle config stuff"""

    @classmethod
    def from_json(cls, json_data):
        """Initialize an object from json."""
        data = json.loads(json_data)
        return cls(data)


class CustomEmojis(Config):
    """A class to handle custom emojis"""

    # This does not have any code because this should just be an alias to Config.
    # I know there are better ways to make this an alias, but this is well enough.


class NoneClass:
    def __init__(self, message):
        self.message = message

    def __getattr__(self, attr):
        print_error(self.message)

