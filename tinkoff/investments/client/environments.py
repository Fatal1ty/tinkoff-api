from enum import Enum

from yarl import URL


class Environment(Enum):
    SANDBOX = 'SANDBOX'
    PRODUCTION = 'PRODUCTION'


EnvironmentURL = {
    Environment.SANDBOX: URL('https://api-invest.tinkoff.ru/openapi/sandbox/'),
    Environment.PRODUCTION: URL('https://api-invest.tinkoff.ru/openapi/'),
}


__all__ = [
    'Environment',
    'EnvironmentURL',
]
