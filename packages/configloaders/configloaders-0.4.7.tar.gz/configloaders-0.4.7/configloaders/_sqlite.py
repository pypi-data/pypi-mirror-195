import ast
import typing
import functools

from ._file import load_from
from ._loader import ConfigLoader
from ._appdir import load_from_appdir

class SqliteConfigLoader(ConfigLoader, suffix='db'):
    TYPES = {
        None: 'NULL',
        int: 'INTEGER',
        float: 'REAL',
        str: 'TEXT',
        bytes: 'BLOB',
        list: 'TEXT'
    }
    def init(self) -> None:
        import sqlite3
        self.sqlite3 = sqlite3
        self.cols = {}
    def search_write(self, data: typing.Dict[str, typing.Any], paths=[]) -> None:
        for k,v in data.items():
            if isinstance(v, dict):
                self.search_write(v, [*paths, k])
            elif isinstance(v, list):
                self.cols['_'.join([*paths, k])] = str(v)
            elif isinstance(v, str):
                self.cols['_'.join([*paths, k])] = f'"{v}"'
            else:
                self.cols['_'.join([*paths, k])] = v
    def write(self, data: typing.Dict[str, typing.Any]) -> None:
        db = self.sqlite3.connect(self.path)
        self.search_write(data)
        db.execute('drop table if exists {}'.format(self.name))
        db.execute('create table {}({})'.format(self.name, ', '.join(['{} {}'.format(k, self.TYPES[type(v)]) for k,v in self.cols.items()])))
        db.execute('insert into {} values ({})'.format(self.name, ', '.join(['?' for _ in self.cols])), list(self.cols.values()))
        db.commit()
    def read(self) -> typing.Dict[str, typing.Any]:
        db = self.sqlite3.connect(self.path)
        cur = db.execute('select * from {}'.format(self.name))
        row = cur.fetchone()
        data = {}
        for i in range(len(cur.description)):
            names = cur.description[i][0].split('_')
            d = data
            for name in names[:-1]:
                d[name] = {}
                d = d[name]
            if isinstance(row[i], str):
                d[names[-1]] = ast.literal_eval(row[i])
            else:
                d[names[-1]] = row[i]
        return data

load_sqlite = functools.partial(load_from, SqliteConfigLoader)
load_sqlite_from_appdir = functools.partial(load_from_appdir, SqliteConfigLoader)