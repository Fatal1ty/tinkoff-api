from enum import Enum
from typing import Optional
from dataclasses import dataclass

from mashumaro import DataClassJSONMixin


class BaseModel(DataClassJSONMixin):
    pass


@dataclass
class Error(BaseModel):
    message: Optional[str]
    code: Optional[str]


class Status(Enum):
    OK = 'Ok'


class Currency(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUS = 'EUR'
