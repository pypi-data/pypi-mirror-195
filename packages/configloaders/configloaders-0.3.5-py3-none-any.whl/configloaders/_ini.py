import ast
import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class INIConfigLoader(FileConfigLoader, suffix='ini'):
    def __init__(self, dir: str, name: str, suffix: str, namespace: typing.Dict[str, typing.Any], save_on_exist: bool, required: bool, untitled: str='UNTITLED') -> None:
        super().__init__(dir, name, suffix, namespace, save_on_exist, required)
        import configparser
        self.configparser = configparser
        self.untitled = untitled
    def literal_quote(self, data: typing.Dict[str, typing.Any]) -> None:
        for k,v in data.items():
            if isinstance(v, str):
                data[k] = f'"{v}"'
            elif isinstance(v, dict):
                self.literal_quote(v)
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        cp = self.configparser.ConfigParser()
        data = {self.untitled: {k:v for k,v in data.items() if not isinstance(v, dict)}, **{k:v for k,v in data.items() if isinstance(v, dict)}}
        self.literal_quote(data)
        cp.read_dict(data)
        cp.write(file)
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        cp = self.configparser.ConfigParser()
        cp.readfp(file)
        return {**{k:ast.literal_eval(v) for k,v in dict(cp.items(self.untitled)).items()}, **{s:{k:ast.literal_eval(v) for k,v in dict(cp.items(s)).items()} for s in cp.sections() if s != self.untitled}}

load_ini = functools.partial(load_from, INIConfigLoader)
load_ini_from_appdir = functools.partial(load_from_appdir, INIConfigLoader)