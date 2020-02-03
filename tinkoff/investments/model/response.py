from dataclasses import dataclass
from typing import Dict, Any

from .base import BaseModel, Status


@dataclass
class TinkoffInvestmentsAPIResponse(BaseModel):
    trackingId: str
    status: Status
    payload: Dict[Any, Any]

    def is_successful(self):
        return self.status is Status.OK
