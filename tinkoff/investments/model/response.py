from dataclasses import dataclass
from typing import Dict, Any

from .base import BaseModel


@dataclass
class TinkoffInvestmentsAPIResponse(BaseModel):
    trackingId: str
    status: str
    payload: Dict[Any, Any]

    def is_successful(self):
        return self.status
