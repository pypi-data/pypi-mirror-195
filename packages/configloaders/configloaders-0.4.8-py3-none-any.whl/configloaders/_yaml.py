import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class YAMLConfigLoader(FileConfigLoader, suffix='yml'):
    def init(self) -> None:
        import yaml
        self.yaml = yaml
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        self.yaml.safe_dump(data, file)
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        return self.yaml.safe_load(file)

load_yaml = functools.partial(load_from, YAMLConfigLoader)
load_yaml_from_appdir = functools.partial(load_from_appdir, YAMLConfigLoader)