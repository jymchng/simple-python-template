# Don't manually change, let poetry-dynamic-versioning handle it.
__version__ = "0.1.0"

__all__ = [
    "Foo",
    "add",
    "NewTypeMethod",
    "NewType",
    "NewInit",
    "NEWTYPE_INIT_ARGS_STR",
    "NEWTYPE_INIT_KWARGS_STR",
    "CUSTOM_GLOBAL",
    "Custom",
]

from simple_python_template._c_extension import Foo, add
from simple_python_template.custom import CUSTOM_GLOBAL, Custom
from simple_python_template.lib import (
    NEWTYPE_INIT_ARGS_STR,
    NEWTYPE_INIT_KWARGS_STR,
    NewInit,
    NewType,
    NewTypeMethod,
)
