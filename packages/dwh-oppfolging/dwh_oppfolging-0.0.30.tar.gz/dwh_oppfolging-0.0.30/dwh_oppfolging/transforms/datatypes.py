"Sub-module for data types"

from dataclasses import dataclass
from typing import Callable, Any, Type


@dataclass
class FieldSchema:
    """
    schema for the extraction of a single datafield
    use together with RecordSchema
    """

    name: str
    dtype: Type
    default: Any = None
    transform: Callable | None = None
    rename: str = ""

    def __post_init__(self):
        if not self.rename:
            self.rename = self.name

    def extract_value(self, mapping: dict) -> Any:
        """
        extracts field value from dict
        >>> FieldSchema('x', int).extract_value({'x': 1})
        1
        >>> FieldSchema('x', int, default='?').extract_value({})
        '?'
        >>> FieldSchema('x', int).rename
        'x'
        """
        value = mapping.get(self.name)
        if value is None:
            return self.default
        if not isinstance(value, self.dtype) and not value is None:
            raise ValueError(f"{self.name} has {type(value)}, expected {self.dtype}")
        if self.transform is not None:
            return self.transform(value)
        return value


@dataclass
class RecordSchema:
    """
    A schema for extracting a record of datafields
    """

    fields: list[FieldSchema]

    def extract_record(self, mapping: dict):
        """
        extracts record from dict
        >>> RecordSchema([FieldSchema('x', int, rename='y')]).extract_record({'x': 1})
        {'y': 1}
        """
        record = {}
        for field in self.fields:
            record[field.rename] = field.extract_value(mapping)
        return record

    def get_field_names(self, renamed_names: bool = False):
        """
        returns field names, optionally the renamed ones
        >>> RecordSchema([FieldSchema('x', int, rename='y')]).get_field_names(True)
        ['y']
        """
        return [field.rename if renamed_names else field.name for field in self.fields]
