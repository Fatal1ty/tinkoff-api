from tinkoff.investments.model.base import Error, Status


class UsageError(ValueError):
    pass


class TinkoffInvestmentsAPIError(Exception):
    def __init__(self, tracking_id: str, status: Status, error: Error):
        self.trackingId = tracking_id
        self.status = status
        self.error = error

    def __str__(self):
        return self.error.code or ''


__all__ = [
    'UsageError',
    'TinkoffInvestmentsAPIError',
]
