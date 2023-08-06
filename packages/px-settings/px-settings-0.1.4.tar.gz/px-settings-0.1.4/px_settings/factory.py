import inspect
from typing import Callable, List, Type, TypeVar
from dataclasses import fields, is_dataclass
from itertools import chain
from functools import reduce, partial
import warnings

from .merger import merge_settings_reducer
from .types import SettingsType
from .updator import update


__all__ = 'settings',

empty = object()
T = TypeVar('T', bound=Type)


def settings(
    *base_sources: List[SettingsType],
    updator: Callable[[T, dict], T] = update
) -> Callable[[T], T]:
    """Decorator for settings class wrapping.

    Result will be a callable, that will generate a resulting settings
    object based on a passed sources.
    """

    def wrapper(base: T) -> T:
        flds = {f.name for f in fields(base)} if is_dataclass(base) else None

        def creator(*current_sources: List[SettingsType], **kwargs: SettingsType):
            sources = list(chain([kwargs], current_sources, base_sources))

            assert len(sources) != 0, (
                'You must provide at least one source object to create '
                'settings instance.'
            )
            result = reduce(merge_settings_reducer, sources)

            if flds is not None:
                result = {k: v for k, v in result.items() if k in flds}

            try:
                instance = base(**result)
            except TypeError as e:
                raise TypeError(
                    f'Settings "{base.__module__}.{base.__name__}" has an invalid input: \r\n{e}'
                )

            if getattr(instance, 'update', empty) is not empty:
                current = inspect.stack()[1]

                warnings.warn(ResourceWarning(
                    f'Settings in "{current.filename}" already have `update` value.',
                    'Update mechanics disabled.',
                    'Use raw `update` function to make update if necessary.',
                ))
            else:
                instance.update = partial(updator, instance)

            return instance

        return creator

    return wrapper
