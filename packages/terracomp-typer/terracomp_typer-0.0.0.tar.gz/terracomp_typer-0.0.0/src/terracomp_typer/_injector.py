"""
Implement dependency injection resolution on functions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import partial
from inspect import signature
from typing import Any, Callable, Container, Dict, Tuple, Type, TypeVar, cast, get_type_hints

T = TypeVar("T")


class DependencyInjectionError(Exception):
    pass


class DependencyInjector(ABC):
    """
    Base class for a dependency injector.
    """

    @staticmethod
    def of(*objects: Any) -> DefaultDependencyInjector:
        return DefaultDependencyInjector(*objects)

    @abstractmethod
    def get_dependency_for_type(self, type_: Type[T]) -> T:
        ...

    def inject(
        self,
        requests: Dict[str, Type[Any]],
        allow_unresolved: bool = True,
        ignore: Container[str] = (),
    ) -> Tuple[Dict[str, Type[Any]], Dict[str, object]]:
        """
        Resolve *requests* to a set of types that have been resolved successfully and another which is the
        same as *requests* minues the resolved keys.
        """

        remaining = {}
        bindings = {}
        for key, value in list(requests.items()):
            if key in ignore:
                remaining[key] = value
            else:
                try:
                    bindings[key] = self.get_dependency_for_type(value)
                except DependencyInjectionError:
                    if not allow_unresolved:
                        raise
                    remaining[key] = value

        return remaining, bindings

    def bind(
        self,
        func: Callable[..., Any],
        allow_unresolved: bool = False,
        ignore: Container[str] = (),
    ) -> Callable[..., Any]:
        """
        Bind dependencies requested through the annotations of *func*.

        :param func: The function to bind dependencies to.
        :param allow_unresolved: Allow unresolved parameters and keep them in the function signature.
        :param ignore: Ignore parameters with these names.
        """

        undefined = object()

        annotations = get_type_hints(func)
        return_annotation = annotations.pop("return", undefined)
        annotations, bindings = self.inject(annotations, allow_unresolved, ignore)

        if not allow_unresolved and annotations:
            raise DependencyInjectionError(...)  # TODO

        if return_annotation is not undefined:
            annotations["return"] = return_annotation

        if not bindings:
            return func

        sig = signature(func)

        bound_func = partial(func, **bindings)
        bound_func.__doc__ = func.__doc__
        bound_func.__annotations__ = annotations
        bound_func.__signature__ = sig.replace(parameters=[v for k, v in sig.parameters.items() if k not in bindings])  # type: ignore[attr-defined]  # noqa: E501
        return bound_func


class DefaultDependencyInjector(DependencyInjector):
    """
    A simple implementation of the #DependencyInjector interface. It can be initialized from a sequence of objects
    that must all be of distinct types, otherwise a #TypeError is raised.
    """

    def __init__(self, *objects: Any) -> None:
        self._mapping: Dict[Type[Any], Any] = {}
        for obj in objects:
            if type(obj) in self._mapping:
                raise TypeError(
                    "cannot populate dependency provider with multiple instances of the same type "
                    f"({type(obj).__name__})"
                )
            self._mapping[type(obj)] = obj

    def get_dependency_for_type(self, type_: Type[T]) -> T:
        if type_ in self._mapping:
            return cast(T, self._mapping[type_])
        raise DependencyInjectionError(f"unable to provide a dependency for type {type_.__name__}")
