import ast
import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class TextLineConfigLoader(FileConfigLoader, suffix='txt'):
    def __init__(self, dir: str, name: str, suffix: str, namespace: typing.Dict[str, typing.Any], save_on_exist: bool, required: bool, quote_string: bool=False) -> None:
        super().__init__(dir, name, suffix, namespace, save_on_exist, required)
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        file.write('\n'.join(map(str, data.values())))
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        result = {}
        lines = file.readlines()
        for i,(k,v) in enumerate(self.filtered_namespace.items()):
            if isinstance(v, str):
                result[k] = lines[i]
            else:
                result[k] = ast.literal_eval(lines[i])
        return result

load_textline = functools.partial(load_from, TextLineConfigLoader)
load_textline_from_appdir = functools.partial(load_from_appdir, TextLineConfigLoader)