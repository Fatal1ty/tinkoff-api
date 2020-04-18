from asyncio import TimeoutError

from tinkoff.investments.model.base import Error, Status


class TinkoffInvestmentsError(Exception):
    pass


class TinkoffInvestmentsUsageError(TinkoffInvestmentsError):
    pass


class TinkoffInvestmentsUnauthorizedError(TinkoffInvestmentsError):
    def __str__(self):
        return 'Have you missed the real token?'


class TinkoffInvestmentsTooManyRequestsError(TinkoffInvestmentsError):
    pass


class TinkoffInvestmentsTimeoutError(TinkoffInvestmentsError, TimeoutError):
    pass


class TinkoffInvestmentsUnavailableError(TinkoffInvestmentsError):
    pass


class TinkoffInvestmentsConnectionError(TinkoffInvestmentsError):
    pass


class TinkoffInvestmentsAPIError(TinkoffInvestmentsError):
    def __init__(self, tracking_id: str, status: Status, error: Error):
        self.trackingId = tracking_id
        self.status = status
        self.error = error

    def __str__(self):
        return f'{self.error.code}, {self.error.message}'


__all__ = [
    'TinkoffInvestmentsError',
    'TinkoffInvestmentsUsageError',
    'TinkoffInvestmentsAPIError',
    'TinkoffInvestmentsUnauthorizedError',
    'TinkoffInvestmentsTooManyRequestsError',
    'TinkoffInvestmentsTimeoutError',
    'TinkoffInvestmentsUnavailableError',
    'TinkoffInvestmentsConnectionError',
]
