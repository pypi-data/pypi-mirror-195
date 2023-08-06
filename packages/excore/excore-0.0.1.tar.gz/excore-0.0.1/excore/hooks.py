from typing import Callable, Sequence, Optional, Union

import inspect
from .registry import HOOKS


def register_hooks(
    hooks: Union[Callable, Sequence[Callable]],
    names: Optional[Union[Callable, Sequence[Callable]]] = None,
    override: bool = False,
):
    if not isinstance(hooks, Sequence):
        hooks = [hooks]
    if isinstance(names, Sequence):
        assert len(names) == len(hooks)
    else:
        names = [None] * len(hooks) if names is None else [names]

    for name, hook in zip(names, hooks):
        HOOKS._register(hook, force=override, name=name)


class Hook:
    __hooks = {}

    def __call__(self, _hooks):
        if not isinstance(_hooks, (tuple, list)):
            _hooks = [_hooks]
        for _hook in _hooks:
            if not (inspect.isfunction(_hook)):
                raise TypeError("Only support function, but got {}".format(type(_hook)))
            name = _hook.__name__
            self.__hooks[name] = _hook
