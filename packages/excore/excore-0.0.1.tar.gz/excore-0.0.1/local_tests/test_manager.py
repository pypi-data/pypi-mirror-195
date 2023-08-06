from core.registry import Registry
from core import logger

MODELS = Registry("Models")
B = Registry("b")


@MODELS.register()
class Res:
    def __init__(self, **kwargs):
        pass


@B.register(name="Res", force=True)
class A:
    pass


print(Registry.get_child("models"))
