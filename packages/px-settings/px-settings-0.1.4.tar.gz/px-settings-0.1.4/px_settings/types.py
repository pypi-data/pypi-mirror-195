from typing import Dict, Union
import sys


__all__ = 'SettingsType',


SettingsType = Union[dict, tuple]


if sys.version_info >= (3, 8):
    from typing import Protocol


    class DataclassType(Protocol):
        __dataclass_fields__: Dict

    SettingsType = Union[dict, tuple, DataclassType]
