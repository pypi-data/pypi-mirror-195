import typing

from .__message import *
from ._file import FileConfigLoader

class ArgParseConfigLoader(FileConfigLoader):
    def __init__(self, namespace: typing.Dict[str, typing.Any], parser=None) -> None:
        super().__init__('', '', None, namespace, False, False)
        import argparse
        self.argparse = argparse
        self.parse_args = parser is None
        self.parser: argparse.ArgumentParser = parser or argparse.ArgumentParser()
        _namespace = namespace
        class Action(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None) -> None:
                paths = self.dest.split('.')
                data = _namespace
                for path in paths[:-1]:
                    data = data[path]
                data[paths[-1]] = values
        self.action = Action
    def search(self, data: typing.Dict[str, typing.Any], paths=[]):
        for k,v in data.items():
            if isinstance(v, dict):
                self.search(v, [*paths, k])
            else:
                self.parser.add_argument('--{}'.format('.'.join([*paths, k])), action=self.action, default=v, type=type(v), metavar=str(v))
    def load(self) -> typing.Any:
        self.search(self.filtered_namespace)
        log_loaded(self.__class__, self.path)
        if self.parse_args:
            self.parser.parse_args()
        return self.parser
    
def load_argparse(namespace, parser=None) -> typing.Any:
    return ArgParseConfigLoader(namespace, parser).load()