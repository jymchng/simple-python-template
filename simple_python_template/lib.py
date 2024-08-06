import logging
import sys
from logging import getLogger
from typing import TYPE_CHECKING


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)s] %(message)s",
    stream=sys.stdout,
)
LOGGER = getLogger("simple_python_template::lib")


NEWTYPE_INIT_ARGS_STR = "_newtype_init_args_"
NEWTYPE_INIT_KWARGS_STR = "_newtype_init_kwargs_"
UNDEFINED = object()

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Type, TypeVar

    T = TypeVar("T")


class NewTypeMethod:
    def __init__(self, func: "Callable", wrapped_cls: "Type"):
        """Initializes the NewTypeMethod with a callable and the class it wraps.

        Args:
            func (Callable): The function to wrap.
            wrapped_cls (Type): The class that the function is associated with.
        """
        if hasattr(func, "__get__"):
            self.func_get = func.__get__
            self.has_get = True
        else:
            self.func_get = func
            self.has_get = False
        self.wrapped_cls = wrapped_cls

    def __get__(self, inst, owner):
        """Retrieves the instance and owner for the descriptor.

        Args:
            inst: The instance of the class.
            owner: The owner class of the descriptor.

        Returns
        -------
            self: The NewTypeMethod instance.
        """
        self.obj = inst
        self.cls = owner
        return self

    def __call__(self, *args, **kwargs):  # noqa: C901
        """Calls the wrapped function, handles the initialization of the wrapped class if necessary.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns
        -------
            The result of the wrapped function or an instance of the wrapped class.
        """
        func = self.func_get(self.obj, self.wrapped_cls) if self.has_get else self.func_get
        has_args = args != ()
        has_kwargs = kwargs != {}
        if not has_args and not has_kwargs:
            result = func()
        if not has_args and has_kwargs:
            result = func(**kwargs)
        if has_args and not has_kwargs:
            result = func(*args)
        if has_args and has_kwargs:
            result = func(*args, **kwargs)
        if isinstance(result, self.wrapped_cls):
            new_type_init_args_str = NEWTYPE_INIT_ARGS_STR
            new_type_init_kwargs_str = NEWTYPE_INIT_KWARGS_STR
            init_args = getattr(self.obj, new_type_init_args_str, None)
            init_kwargs = getattr(self.obj, new_type_init_kwargs_str, None)
            has_init_args = init_args is not None
            has_init_kwargs = init_kwargs is not None
            if not has_init_args and not has_init_kwargs:
                return self.cls(result)
            if not has_init_args and has_init_kwargs:
                return self.cls(result, **init_kwargs)
            if has_init_args and not has_init_kwargs:
                return self.cls(result, *init_args)
            if has_init_args and has_init_kwargs:
                return self.cls(result, *init_args, **init_kwargs)
        return result


class NewInit:
    def __init__(self, constructor):
        """

        Initializes the NewInit with a constructor.

        Args:
            constructor: The constructor to wrap.
        """
        if hasattr(constructor, "__get__"):
            self.func_get = constructor.__get__
            self.has_get = True
        else:
            self.func_get = constructor
            self.has_get = False

    def __get__(self, obj, owner):
        """Retrieves the object and owner for the descriptor.

        Args:
            obj: The instance of the class.
            owner: The owner class of the descriptor.

        Returns
        -------
            self: The NewInit instance.
        """
        self.obj = obj
        self.cls = owner
        return self

    def __call__(self, *constructor_args, **constructor_kwargs):
        """Calls the wrapped constructor with the provided arguments.

        Args:
            *constructor_args: Positional arguments to pass to the constructor.
            **constructor_kwargs: Keyword arguments to pass to the constructor.
        """
        new_type_constructor_args_str = NEWTYPE_INIT_ARGS_STR
        new_type_constructor_kwargs_str = NEWTYPE_INIT_KWARGS_STR

        func = self.func_get(self.obj, self.cls) if self.has_get else self.func_get
        LOGGER.debug("func: ", func)
        has_args = constructor_args != ()
        has_kwargs = constructor_kwargs != {}
        LOGGER.debug("constructor_args: ", constructor_args)
        LOGGER.debug("constructor_kwargs: ", constructor_kwargs)
        setattr(self.obj, new_type_constructor_args_str, constructor_args[1:]) if not hasattr(
            self.obj, new_type_constructor_args_str
        ) else None
        setattr(self.obj, new_type_constructor_kwargs_str, constructor_kwargs) if not hasattr(
            self.obj, new_type_constructor_kwargs_str
        ) else None
        if not has_args and not has_kwargs:
            func()
        if not has_args and has_kwargs:
            func(**constructor_kwargs)
        if has_args and not has_kwargs:
            func(*constructor_args)
        if has_args and has_kwargs:
            func(*constructor_args, **constructor_kwargs)

        LOGGER.debug("self.obj; type(self.obj): ", self.obj, type(self.obj))
        LOGGER.debug("self.obj._newtype_init_kwargs_: ", self.obj._newtype_init_kwargs_)


def NewType(  # noqa: C901,N802
    type_: "Type[T]",  # noqa: N802
    **context: "Dict[str, Any]",
) -> "Type[T]":  # noqa: D205
    """Creates a new type used to define new types with additional behavior.

    Args:
        type_ (Type[T]): The base type to create a new type from.
        **context: Additional context for the new type.

    Returns
    -------
        tNT: A new type that behaves like the specified base type.
    """

    class BaseBaseNewType(type_):  # type: ignore[valid-type, misc]
        def __init_subclass__(cls, **context) -> None:
            super().__init_subclass__(**context)
            for k, v in type_.__dict__.items():
                if callable(v) and k not in object.__dict__:
                    setattr(cls, k, NewTypeMethod(v, type_))
                elif k not in object.__dict__:
                    setattr(cls, k, v)
            cls.__init__ = NewInit(cls.__init__)  # type: ignore[method-assign]

    class BaseNewType(BaseBaseNewType):
        def __new__(cls, value, *_args, **_kwargs):
            LOGGER.debug("__new__: ", type_, cls, value, _args, _kwargs)
            if type_.__new__ == object.__new__:
                inst = type_.__new__(cls)
                value_dict: dict = getattr(value, "__dict__", UNDEFINED)
                if value_dict is not UNDEFINED:
                    for k, v in value_dict.items():
                        setattr(inst, k, v)
                value_slots: tuple = getattr(value, "__slots__", UNDEFINED)
                if value_slots is not UNDEFINED:
                    for k in value_slots:
                        v = getattr(value, k, UNDEFINED)
                        if v is not UNDEFINED:
                            setattr(inst, k, v)
            else:
                inst = type_.__new__(cls, value)
            return inst

        def __init__(self, _value, *_args, **_kwargs): ...

    return BaseNewType
