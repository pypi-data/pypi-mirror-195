import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class TOMLConfigLoader(FileConfigLoader, suffix='toml'):
    def init(self) -> None:
        import toml
        self.toml = toml
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        self.toml.dump(data, file)
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        return self.toml.load(file)

load_toml = functools.partial(load_from, TOMLConfigLoader)
load_toml_from_appdir = functools.partial(load_from_appdir, TOMLConfigLoader)