from enum import Enum
from dataclasses import dataclass

# Used for request and response for now
@dataclass
class FuelTypeEnum(Enum):
    E10 = "E10"
    E5 = "E5"
    B10 = "B10"
    B7Standard = "B7Standard"
    B7Premium = "B7Premium"
    HVO = "HVO"
