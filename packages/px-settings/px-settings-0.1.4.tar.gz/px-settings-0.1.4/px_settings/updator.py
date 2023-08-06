from typing import Type, TypeVar


__all__ = 'update',

T = TypeVar('T', bound=Type)


def update(settings: T, **data: dict) -> T:
    for key in data:
        setattr(settings, key, data[key])

    return settings
