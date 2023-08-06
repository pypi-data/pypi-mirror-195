import os
import typing

from .__message import *
from .__util import abstract
from ._loader import ConfigLoader


class FileConfigLoader(ConfigLoader):
    def __init_subclass__(cls, suffix: typing.Union[str, None]=None, binary: bool=False) -> None:
        super().__init_subclass__(suffix)
        cls.rmode = 'rb' if binary else 'r'
        cls.wmode = 'wb' if binary else 'w'
    def load(self) -> typing.Any:
        if self.required and not os.path.exists(self.path):
            self.dump()
        elif not abstract(self.read) and (self.required or os.path.exists(self.path)):
            with open(self.path, self.rmode) as file:
                data = self.read(file)
                if data is not None:
                    for key in data:
                        if key in self.filtered_namespace:
                            self.namespace[key] = data[key]
                    log_loaded(self.__class__, self.path)
                else:
                    log_failed(self.__class__, self.path, None)
        return self.namespace
    def dump(self, original: bool=False) -> None:
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if not abstract(self.write):
            with open(self.path, self.wmode) as file:
                self.write(file, self.original_filtered_namespace if original else self.filtered_namespace)
                log_saved(self.__class__, self.path)
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None: pass
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]: pass

loader_list: typing.List[FileConfigLoader] = []

def load_from(loader_class: typing.Type[FileConfigLoader], namespace, dir='.', name='config', suffix=None, save_on_exit=False, required=False, **kwargs) -> FileConfigLoader:
    loader = loader_class(dir, name, suffix, namespace, save_on_exit, required, **kwargs)
    loader.load()
    loader_list.append(loader)
    return loader

def dump(original: bool=False) -> None:
    for loader in loader_list:
        loader.dump(original=original)