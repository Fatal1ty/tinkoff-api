from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

import ciso8601
from mashumaro import DataClassJSONMixin
from mashumaro.types import SerializableType


class BaseModel(DataClassJSONMixin):
    pass


@dataclass
class Error(BaseModel):
    message: Optional[str] = None
    code: Optional[str] = None


class Status(Enum):
    OK = 'Ok'
    ERROR = 'Error'


class Currency(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUS = 'EUR'


class ISODateTime(datetime, SerializableType):

    def _serialize(self):
        return self.isoformat()

    @classmethod
    def _deserialize(cls, value):
        return ciso8601.parse_datetime(value)
