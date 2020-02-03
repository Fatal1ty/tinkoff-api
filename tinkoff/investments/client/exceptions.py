from tinkoff.investments.model.base import Error


class UsageError(ValueError):
    pass


class TinkoffInvestmentsAPIError(Exception):
    def __init__(self, tracking_id: str, status: str, error: Error):
        self.trackingId = tracking_id
        self.status = status
        self.error = error


__all__ = [
    'UsageError',
    'TinkoffInvestmentsAPIError',
]
