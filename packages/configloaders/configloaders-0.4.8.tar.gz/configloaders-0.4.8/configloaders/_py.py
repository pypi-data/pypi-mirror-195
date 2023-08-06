import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class PYConfigLoader(FileConfigLoader, suffix='py'):
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        import importlib.util
        spec = importlib.util.spec_from_file_location(self.path, self.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return vars(module)

load_py = functools.partial(load_from, PYConfigLoader)
load_py_from_appdir = functools.partial(load_from_appdir, PYConfigLoader)