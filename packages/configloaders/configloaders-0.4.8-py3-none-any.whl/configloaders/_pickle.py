import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class PickleConfigLoader(FileConfigLoader, suffix='pkl', binary=True):
    def init(self) -> None:
        import pickle
        self.pickle = pickle
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        self.pickle.dump(data, file)
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        return self.pickle.load(file)

load_pkl = functools.partial(load_from, PickleConfigLoader)
load_pkl_from_appdir = functools.partial(load_from_appdir, PickleConfigLoader)