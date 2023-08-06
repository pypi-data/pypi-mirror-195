__version__ = "0.0.0"

from ._build import build_app_from_module
from ._injector import DependencyInjectionError, DependencyInjector

__all__ = [
    "DependencyInjectionError",
    "DependencyInjector",
    "build_app_from_module",
]
