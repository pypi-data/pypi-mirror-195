import ast
import typing
import gettext

from .__message import *
from ._file import ConfigLoader, load_from

class TkinterConfigLoader(ConfigLoader):
    def __init__(self, namespace: typing.Dict[str, typing.Any], title=gettext.gettext('Config'), icon=None, topmost=False) -> None:
        super().__init__('', '', None, namespace, False, False)
        self.title = title
        self.icon = icon
        self.topmost = topmost
    def confirm(self):
        import tkinter.messagebox
        namespace = {}
        def read(node, dest, k, v):
            if 'children' in v:
                dest[k] = {}
                for _k,_v in v['children'].items():
                    read(node[k], dest[k], _k, _v)
            else:
                _v = v['entry'].get()
                _type = type(node[k])
                try:
                    if not isinstance(node[k], str):
                        _v = ast.literal_eval(_v)
                    dest[k] = _type(_v)
                except:
                    tkinter.messagebox.showwarning(gettext.gettext('Warning'), gettext.gettext('"{name}" must be type of {type}').format(name=_v, type=_type))
                    return False
            return True
        for k,v in self.tk_namespace.items():
            if not read(self.filtered_namespace, namespace, k, v):
                return
        for k in namespace:
            if k in self.filtered_namespace:
                self.namespace[k] = namespace[k]
        self.tk.destroy()
        log_loaded(self.__class__, self.path)
        self.load_flag = True
    def cancel(self):
        self.tk.destroy()
        self.load_flag = False
    def add_option(self, body, namespace, i, k, v):
        if k not in namespace:
            namespace[k] = {}
        if not isinstance(v, dict):
            self.tkinter.Label(body, text=k).grid(row=i, column=0)
            entry = self.tkinter.Entry(body)
            entry.insert(0, str(v))
            entry.grid(row=i, column=1)
            body.grid_rowconfigure(i, pad=3)
            namespace[k]['entry'] = entry
        else:
            namespace[k]['children'] = {}
            self.tkinter.Label(body, text=k).grid(row=i, column=0)
            _body = self.tkinter.Frame(body)
            _body.grid(row=i, column=1)
            for _i,(_k,_v) in enumerate(v.items()):
                self.add_option(_body, namespace[k]['children'], _i, _k, _v)
    def load(self) -> typing.Any:
        import tkinter
        self.tkinter = tkinter
        tk = tkinter.Tk()
        self.tk = tk
        tk.title(self.title)
        tk.iconbitmap(self.icon)
        tk.attributes("-topmost", self.topmost)
        body = tkinter.Frame(tk, padx=10, pady=10)
        body.pack()
        self.tk_namespace = {}
        for i,(k,v) in enumerate(self.filtered_namespace.items()):
            self.add_option(body, self.tk_namespace, i, k, v)
        footer = tkinter.Frame(tk, padx=10, pady=10)
        footer.pack(fill='x')
        tkinter.Button(footer, text=gettext.gettext('Confirm'), command=self.confirm).pack(side='right')
        tkinter.Frame(footer, width=5).pack(side='right')
        tkinter.Button(footer, text=gettext.gettext('Cancel'), command=self.cancel).pack(side='right')
        self.tk.mainloop()
        return self.load_flag
    
def load_tkinter(namespace, title: typing.Union[str, None]=None, icon=None, topmost=None) -> typing.Any:
    loader = TkinterConfigLoader(**{k: v for k, v in locals().items() if v is not None})
    return loader, loader.load()