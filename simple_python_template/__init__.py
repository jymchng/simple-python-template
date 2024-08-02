# Don't manually change, let poetry-dynamic-versioning handle it.
__version__ = "0.0.0"

__all__: list[str] = []

from typing import TYPE_CHECKING, Protocol

NEWTYPE_INIT_ARGS_STR = "_newtype_init_args_"
NEWTYPE_INIT_KWARGS_STR = "_newtype_init_kwargs_"
UNDEFINED = object()

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Tuple, Type, TypeVar

    GenericTypeType = TypeVar("GenericTypeType", type)

    class NewTypeObject(Protocol):
        _args_: "Tuple[Any, ...]"
        _kwargs_: "Dict[str, Any]"


class NewTypeMethod:
    def __init__(self, func: "Callable", wrapped_cls: "Type"):
        if hasattr(func, "__get__"):
            self.func_get = func.__get__
            self.has_get = True
        else:
            self.func_get = func
            self.has_get = False
        self.wrapped_cls = wrapped_cls

    def __get__(self, inst, owner):
        self.obj: NewTypeObject = inst
        self.cls: Type[NewTypeObject] = owner
        return self

    def __call__(self, *args, **kwargs):
        if self.has_get:
            func = self.func_get(self.obj, self.wrapped_cls)
        else:
            func = self.func_get
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
            print(has_init_args, has_init_kwargs)
            print(init_args, init_kwargs)
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
        if hasattr(constructor, "__get__"):
            self.func_get = constructor.__get__
            self.has_get = True
        else:
            self.func_get = constructor
            self.has_get = False

    def __get__(self, obj, owner):
        self.obj: NewTypeObject = obj
        self.cls: Type[NewTypeObject] = owner
        return self

    def __call__(self, *constructor_args, **constructor_kwargs):
        new_type_constructor_args_str = NEWTYPE_INIT_ARGS_STR
        new_type_constructor_kwargs_str = NEWTYPE_INIT_KWARGS_STR

        if self.has_get:
            func = self.func_get(self.obj, self.cls)
        else:
            func = self.func_get
        print("func: ", func)
        has_args = constructor_args != ()
        has_kwargs = constructor_kwargs != {}
        print("constructor_args: ", constructor_args)
        print("constructor_kwargs: ", constructor_kwargs)
        setattr(self.obj, new_type_constructor_args_str, constructor_args[1:]) if not hasattr(
            self.obj, new_type_constructor_args_str
        ) else None
        setattr(self.obj, new_type_constructor_kwargs_str, constructor_kwargs) if not hasattr(
            self.obj, new_type_constructor_kwargs_str
        ) else None
        # constructor_args = (getattr(self.obj, new_type_constructor_args_str, UNDEFINED) is not UNDEFINED) or constructor_args
        # constructor_kwargs = (getattr(self.obj, new_type_constructor_kwargs_str, UNDEFINED) is not UNDEFINED) or constructor_kwargs
        if not has_args and not has_kwargs:
            func()
        if not has_args and has_kwargs:
            func(**constructor_kwargs)
        if has_args and not has_kwargs:
            func(*constructor_args)
        if has_args and has_kwargs:
            func(*constructor_args, **constructor_kwargs)

        print("self.obj; type(self.obj): ", self.obj, type(self.obj))
        print("self.obj._newtype_init_kwargs_: ", self.obj._newtype_init_kwargs_)


def NewType(type_: "GenericTypeType", **context) -> "GenericTypeType":
    class BaseBaseNewType(type_):
        def __init_subclass__(cls, **context) -> None:
            super().__init_subclass__(**context)
            for k, v in type_.__dict__.items():
                if callable(v) and k not in object.__dict__:
                    setattr(cls, k, NewTypeMethod(v, type_))
                elif k not in object.__dict__:
                    setattr(cls, k, v)
            cls.__init__ = NewInit(cls.__init__)
            return cls

    class BaseNewType(BaseBaseNewType):
        def __new__(cls, value, *_args, **_kwargs):
            print("__new__: ", type_, cls, value, _args, _kwargs)
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
