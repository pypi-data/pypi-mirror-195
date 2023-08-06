import typing

from ._file import FileConfigLoader, load_from

def load_from_appdir(loader: typing.Type[FileConfigLoader], appname, appauthor, namespace, name='config', suffix=None, save_on_exit=True, required=False, **kwargs) -> typing.Any:
    import appdirs
    dir = appdirs.user_config_dir(appname, appauthor)
    return load_from(loader, namespace, dir, name, suffix, save_on_exit, required, **kwargs)