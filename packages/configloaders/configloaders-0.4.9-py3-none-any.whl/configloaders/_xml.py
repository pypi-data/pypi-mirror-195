import ast
import typing
import functools

from ._appdir import load_from_appdir
from ._file import FileConfigLoader, load_from

class XMLConfigLoader(FileConfigLoader, suffix='xml'):
    def init(self) -> None:
        import xml.etree.cElementTree
        self.tree = xml.etree.cElementTree
    def search_write(self, root, data: typing.Dict[str, typing.Any]) -> None:
        root: self.tree.Element = root
        for k,v in data.items():
            e = self.tree.Element(k)
            root.append(e)
            if not isinstance(v, dict):
                e.text = f'"{v}"' if isinstance(v, str) else str(v)
            else:
                self.search_write(e, v)
    def search_read(self, root, data: dict) -> None:
        root: self.tree.Element = root
        for e in root.findall('*'):
            childs = e.findall('*')
            if len(childs) == 0:
                data[e.tag] = ast.literal_eval(e.text)
            else:
                data[e.tag] = {}
                self.search_read(e, data[e.tag])
    def write(self, file: typing.TextIO, data: typing.Dict[str, typing.Any]) -> None:
        root = self.tree.Element('root')
        self.search_write(root, data)
        self.tree.ElementTree(root).write(self.path)
    def read(self, file: typing.TextIO) -> typing.Dict[str, typing.Any]:
        tree = self.tree.parse(file)
        data = {}
        self.search_read(tree.getroot(), data)
        return data
    
load_xml = functools.partial(load_from, XMLConfigLoader)
load_xml_from_appdir = functools.partial(load_from_appdir, XMLConfigLoader)