import importlib
import pkgutil


def auto_import(path: str):
    for _, name, _ in pkgutil.iter_modules([path]):
        importlib.import_module(f'{path.replace('/', '.')}.{name}')
