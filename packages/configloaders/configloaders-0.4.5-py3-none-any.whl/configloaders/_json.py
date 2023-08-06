import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class JSONConfigLoader(FileConfigLoader, suffix='json'):
    def init(self) -> None:
        import json
        self.json = json
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        self.json.dump(data, file)
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        return self.json.load(file)
    def filter(self, key: str, value: typing.Any) -> bool:
        b = super().filter(key, value)
        if b: self.json.dumps(value)
        return b
    
load_json = functools.partial(load_from, JSONConfigLoader)
load_json_from_appdir = functools.partial(load_from_appdir, JSONConfigLoader)