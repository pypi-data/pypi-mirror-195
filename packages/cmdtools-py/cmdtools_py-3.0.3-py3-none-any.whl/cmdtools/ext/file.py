from __future__ import annotations

import importlib
import importlib.util
import inspect
import os
from typing import Callable

from cmdtools.callback import Callback
from cmdtools.ext.command import Command, Container, GroupWrapper


class ModuleLoader(Container):
    """A command module loader class.

    Parameters
    ----------
    fpath : str
        Path to the command file.
    load_classes : bool
        Loads command classes in the module if true,
        if false just load the whole file as a command module.

    Raises
    ------
    NameError
        If not loading command classes, and callback is not set.
    """

    def __init__(self, fpath: str, *, load_classes: bool = True):
        self.path = fpath
        super().__init__()

        # load module directly from source file with the exec_module() method
        spec = importlib.util.spec_from_file_location(
            fpath.rsplit(os.sep, 1)[-1].rstrip(".py"), fpath
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if load_classes:
            for _, obj in module.__dict__.items():
                if inspect.isclass(obj) and obj.__module__ == spec.name:
                    if Command in inspect.getmro(obj):
                        self.commands.append(obj())
        else:
            wrapper = GroupWrapper(spec.name, getattr(module, "__aliases__", None))
            callfunc: Callable = getattr(module, spec.name, None)

            if callfunc:
                wrapper._callback = Callback(callfunc)
            else:
                raise NameError("Could not load callback")

            self.commands.append(wrapper)
