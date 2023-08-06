from __future__ import annotations

from functools import wraps
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Any, Callable, Mapping, Sequence

from typer import Exit, Typer

from ._injector import DependencyInjector


def build_app_from_module(
    module_name: str,
    name: str | None = None,
    typer_options: Mapping[str, Any] | None = None,
    dependencies: DependencyInjector | Sequence[Any] = (),
) -> Typer:
    """
    Looks at the module given with *module_name* and adds subcommand groups or commands to the Typer *app* based on
    the contents. Packages with an `__init__.py` will create a subcommand group, where the docstring of that module
    is the help of the group. Python modules that don't start with an underscore will create a command in the current
    subcommand group.

    :param module_name: The module to create a #Typer application for. The module must be a package with submodules.
    :param name: Override the name of the root #Typer application.
    :param typer_options: Keyword arguments to pass to every #Typer creation.
    :param dependencies: A sequence of objects with unique types that are injected into commands based on their
        function signature.
    """

    if not isinstance(dependencies, DependencyInjector):
        dependencies = DependencyInjector.of(*dependencies)

    module = import_module(module_name)
    assert module.__file__, f"module {module_name!r} has no __file__"
    assert Path(module.__file__).stem == "__init__", f"expected a package for {module_name!r}"

    name = name or module_name.rpartition(".")[-1]
    app = Typer(name=name, help=module.__doc__, **(typer_options or {}))

    for submodule_info in iter_modules(module.__path__, prefix=module_name + "."):
        subcommand_name = submodule_info.name.rpartition(".")[-1]
        module_spec = submodule_info.module_finder.find_spec(submodule_info.name, module.__path__)  # type: ignore  # noqa: E501
        assert module_spec is not None, f"unable to find module spec of {submodule_info.name!r}"
        assert module_spec.origin is not None, f"module spec of {submodule_info.name!r} has no origin"

        if Path(module_spec.origin).stem == "__init__":
            sub_app = build_app_from_module(
                submodule_info.name,
                typer_options=typer_options,
                dependencies=dependencies,
            )
            app.add_typer(sub_app)
        elif not subcommand_name.startswith("_"):
            submodule = import_module(submodule_info.name)
            func = dependencies.bind(submodule.main, allow_unresolved=True)
            func = _raise_non_zero_exit_code_as_exit(func)
            app.command(
                name=subcommand_name,
                help=func.__doc__ or submodule.__doc__,
            )(func)

    return app


def _raise_non_zero_exit_code_as_exit(func: Callable[..., int | None]) -> Callable[..., None]:
    """
    Wraps a function to raise a #Exit exception at the end.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> None:
        result = func(*args, **kwargs)
        if isinstance(result, int):
            raise Exit(code=result)
        elif result is not None:
            raise RuntimeError("expected None or integer return value from command function")
        raise Exit()

    return wrapper
