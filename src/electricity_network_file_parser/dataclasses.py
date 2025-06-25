from dataclasses import dataclass
from typing import List

@dataclass
class PropertyDescription:
    property_type : str
    property_attributes : dict

@dataclass
class EntityDescription7x:
    row_number : int
    entity_columns : List[str]