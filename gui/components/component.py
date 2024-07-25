import re
import inspect
from contextlib import suppress
from pathlib import Path
from . import QWidget
from .settings import settings


class Component(type(QWidget)):
    class Partial:
        def __init__(self, external_class, _component_alignment=None):
            self.external_class = external_class
            self._component_alignment = _component_alignment

        def __call__(self, *regular_args, **kwargs):
            instance = self.external_class.__new__(self.external_class)
            instance._component_alignment = self._component_alignment
            instance.__init__(*regular_args, **kwargs)

            directory = Component.retrieve_kwargs(instance.__init__)
            directory.update(kwargs)

            with suppress(FileNotFoundError):
                filename = Path(instance.__init__.__globals__["__file__"]).stem
                css = open(f"{settings.stylesheets_directory}/{filename}.css").read()
                instance.setStyleSheet(Component.inject_settings(directory, css))
            return instance

    def retrieve_kwargs(func):
        signature = inspect.signature(func)
        return {
            param.name: param.default
            for param in signature.parameters.values()
            if param.default != inspect.Parameter.empty
        }

    def inject_settings(dictionary, text, pattern=r"\((\w+)\)"):
        return re.sub(pattern, lambda match: str(dictionary[match.group(1)]), text)

    def __getitem__(external_class, special_value):
        return Component.Partial(external_class, special_value)

    def __call__(external_class, *args, **kwargs):
        return Component.Partial(external_class)(*args, **kwargs)
