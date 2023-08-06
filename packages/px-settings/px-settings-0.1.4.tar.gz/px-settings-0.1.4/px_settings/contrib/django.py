from typing import Callable, List, Type, TypeVar
from django.conf import settings as django_settings
from px_settings import settings as base_settings, update as base_update
from px_settings.types import SettingsType


__all__ = 'collect_prefixed', 'collect_sources', 'update', 'settings',

T = TypeVar('T', bound=Type)
DELIMITER = '_'


# [TODO]: Update px_settings.contrib.django.collect_prefixed to be able to
# resolve from dict, not only an object based resolver.
# Or make a base prefix resolver for dicts and use it in django-related
# version.
def collect_prefixed(obj: object, prefix: str) -> dict:
    strip_by = len(prefix)
    storage = obj._wrapped if hasattr(obj, '_wrapped') else obj

    return {
        key[strip_by:]: value
        for key, value in storage.__dict__.items()
        if key.startswith(prefix)
    }


def collect_sources(
    name: str,
    delimiter: str = DELIMITER,
    settings_module = django_settings
) -> List[dict]:
    assert settings_module.configured is True, 'Configure django settings first.'

    return (
        collect_prefixed(settings_module, name + delimiter),
        getattr(settings_module, name, {}),
    )


def update(
    name: str,
    delimiter: str,
    settings_module,
    settings: T,
    data: dict
) -> T:
    prefixed, from_dict = collect_sources(
        name, delimiter=delimiter, settings_module=settings_module
    )

    return base_update(settings, **{**from_dict, **prefixed, **data})


def settings(
    name: str,
    *sources: List[SettingsType],
    updator: Callable[[T, dict], T] = update,
    delimiter: str = DELIMITER,
    settings_module = django_settings
) -> Callable[[T], T]:
    return base_settings(
        *collect_sources(
            name, delimiter=delimiter, settings_module=settings_module
        ),
        *sources,
        updator=lambda settings, **data: updator(
            name,
            delimiter,
            settings_module,
            settings,
            data
        )
    )
