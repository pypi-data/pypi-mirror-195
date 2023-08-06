import os
import copy
import types
import typing
import atexit

from .__message import *
from .__util import abstract

class ConfigLoader:
    def __init__(self, dir: str, name: str, suffix: str, namespace: typing.Dict[str, typing.Any], save_on_exist: bool, required: bool) -> None:
        self.dir = dir
        self.name = name
        self.suffix = suffix or self.suffix
        self.path = os.path.join(self.dir, self.name)
        self.namespace = namespace
        self.required = required
        if self.suffix is not None:
            self.path += f'.{self.suffix}'
        if save_on_exist:
            atexit.register(self.dump)
        self.init()
        self.original_filtered_namespace = copy.deepcopy(self.filtered_namespace)
    def __init_subclass__(cls, suffix: typing.Union[str, None]=None) -> None:
        cls.suffix = suffix
    @property
    def filtered_namespace(self) -> typing.Dict[str, typing.Any]:
        return copy.deepcopy({k:v for k,v in self.namespace.items() if self.serializable(k, v)})
    def serializable(self, key: str, value: typing.Any) -> bool:
        try:
            return self.filter(key, value)
        except Exception as e:
            log_failed(key, value, e)
        return False
    def load(self) -> typing.Any:
        if self.required and not os.path.exists(self.path):
            self.dump()
        elif not abstract(self.read) and (self.required or os.path.exists(self.path)):
            data = self.read()
            for key in data:
                if key in self.filtered_namespace:
                    self.namespace[key] = data[key]
            log_loaded(self.__class__, self.path)
        return self.namespace
    def dump(self, original: bool=False) -> None:
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if not abstract(self.write):
            self.write(self.original_filtered_namespace if original else self.filtered_namespace)
            log_saved(self.__class__, self.path)
    def init(self) -> None: pass
    def write(self, data: typing.Dict[str, typing.Any]) -> None: pass
    def read(self) -> typing.Dict[str, typing.Any]: pass
    def filter(self, key: str, value: typing.Any) -> bool: 
        return not key.startswith('_') and not isinstance(value, types.ModuleType)