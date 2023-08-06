from dataclasses import is_dataclass

from .types import SettingsType


__all__ = 'merge_dicts', 'resolve_dict', 'merge_settings_reducer',


def merge_dicts(a: dict, b: dict) -> dict:
    return {**b, **a}


def resolve_dict(settings: SettingsType) -> dict:
    """Transforms some internal types like nametuples and dataclasses
    into a plain dict.
    """
    if hasattr(settings, '_asdict'):
        return settings._asdict()

    if is_dataclass(settings):
        return dict(settings.__dict__)

    return settings


def merge_settings_reducer(a: SettingsType, b: SettingsType) -> dict:
    return merge_dicts(resolve_dict(a), resolve_dict(b))
