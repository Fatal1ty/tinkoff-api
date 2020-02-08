from dataclasses import dataclass
from typing import Any

from .base import BaseModel, Status


@dataclass
class TinkoffInvestmentsAPIResponse(BaseModel):
    trackingId: str
    status: Status
    payload: Any

    def is_successful(self):
        return self.status is Status.OK
