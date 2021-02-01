# tinkoff-api

> Python Tinkoff API client for asyncio and humans.

[![build](https://github.com/Fatal1ty/tinkoff-api/workflows/build/badge.svg)](https://github.com/Fatal1ty/tinkoff-api/actions?query=workflow%3Abuild)
[![Latest Version](https://img.shields.io/pypi/v/tinkoff-api.svg)](https://pypi.python.org/pypi/tinkoff-api)
[![Python Version](https://img.shields.io/pypi/pyversions/tinkoff-api.svg)](https://pypi.python.org/pypi/tinkoff-api)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Table of contens
--------------------------------------------------------------------------------
* [Covered APIs](#covered-apis)
* [Features](#features)
* [Installation](#installation)
* [Usage examples](#usage-examples)
    * [REST API client](#rest-api-client)
    * [Streaming client](#streaming-client)
    * [Dynamic subscriptions in runtime](#dynamic-subscriptions-in-runtime)
    * [Complete simple bot](#complete-simple-bot)
    * [Historical data](#historical-data)
* [TODO](#todo)


Covered APIs
--------------------------------------------------------------------------------
* Tinkoff Investments ([official docs](https://tinkoffcreditsystems.github.io/invest-openapi/))


Features
--------------------------------------------------------------------------------
* Clients for both [REST](https://tinkoffcreditsystems.github.io/invest-openapi/rest/) and [Streaming](https://tinkoffcreditsystems.github.io/invest-openapi/marketdata/) protocols in Tinkoff Investments
* Presence of data classes for all interaction with API
* Automatic reconnection and keep-alive connections
* Internal exclusive rate limiter for every resource in REST protocol
* Friendly exceptions for API errors


Installation
--------------------------------------------------------------------------------

Use pip to install:
```shell
$ pip install tinkoff-api
```

Usage examples
--------------------------------------------------------------------------------

#### REST API client:
```python
import asyncio
from datetime import datetime
from tinkoff.investments import (
    TinkoffInvestmentsRESTClient,
    Environment,
    CandleResolution,
)
from tinkoff.investments.client.exceptions import TinkoffInvestmentsError


async def show_apple_year_candles():
    try:
        async with TinkoffInvestmentsRESTClient(
            token="TOKEN", environment=Environment.SANDBOX
        ) as client:

            candles = await client.market.candles.get(
                figi="BBG000B9XRY4",
                dt_from=datetime(2019, 1, 1),
                dt_to=datetime(2019, 12, 31),
                interval=CandleResolution.DAY,
            )
            for candle in candles:
                print(f"{candle.time}: {candle.h}")
    except TinkoffInvestmentsError as e:
        print(e)


async def jackpot():
    try:
        async with TinkoffInvestmentsRESTClient(
            token="TOKEN", environment=Environment.SANDBOX
        ) as client:

            instruments = await client.market.instruments.search("AAPL")
            apple = instruments[0]

            account = await client.sandbox.accounts.register()
            await client.sandbox.accounts.positions.set_balance(
                figi=apple.figi,
                balance=100,
                broker_account_id=account.brokerAccountId,
            )

            print("We created the following portfolio:")
            positions = await client.portfolio.get_positions()
            for position in positions:
                print(f"{position.name}: {position.lots} lots")
    except TinkoffInvestmentsError as e:
        print(e)


asyncio.run(jackpot())
```

#### Streaming Client:
```python
import asyncio
from datetime import datetime
from tinkoff.investments import (
    CandleEvent,
    CandleResolution,
    TinkoffInvestmentsStreamingClient,
)

client = TinkoffInvestmentsStreamingClient(token="TOKEN")


@client.events.candles("BBG009S39JX6", CandleResolution.MIN_1)
@client.events.candles("BBG000B9XRY4", CandleResolution.MIN_1)
async def on_candle(candle: CandleEvent, server_time: datetime):
    print(candle, server_time)


asyncio.run(client.run())
```

#### Dynamic subscriptions in runtime:
```python
import asyncio
from datetime import datetime
from tinkoff.investments import (
    CandleEvent,
    CandleResolution,
    TinkoffInvestmentsStreamingClient,
)

client = TinkoffInvestmentsStreamingClient(token="TOKEN")


@client.events.candles("BBG000B9XRY4", CandleResolution.HOUR)
async def on_candle(candle: CandleEvent, server_time: datetime):
    if candle.h > 1000:
        await client.events.candles.subscribe(
            callback=on_candle,
            figi=candle.figi,
            interval=CandleResolution.MIN_1,
        )
    elif candle.h < 1000:
        await client.events.candles.unsubscribe(
            candle.figi, CandleResolution.MIN_1
        )


asyncio.run(client.run())
```

#### Complete simple bot:
```python
import asyncio
from datetime import datetime

from tinkoff.investments import (
    CandleEvent,
    CandleResolution,
    OperationType,
    TinkoffInvestmentsRESTClient,
    TinkoffInvestmentsStreamingClient,
)

streaming = TinkoffInvestmentsStreamingClient("TOKEN")
rest = TinkoffInvestmentsRESTClient("TOKEN")


@streaming.events.candles("BBG000B9XRY4", CandleResolution.MIN_1)
async def buy_apple(candle: CandleEvent, server_time: datetime):
    if candle.c > 350:
        await rest.orders.create_market_order(
            figi="BBG000B9XRY4",
            lots=1,
            operation=OperationType.BUY,
            broker_account_id=123,
        )


asyncio.run(streaming.run())
```

#### Historical data:
```python
import asyncio
from datetime import datetime

from tinkoff.investments import (
    CandleResolution,
    Environment,
    TinkoffInvestmentsRESTClient,
)
from tinkoff.investments.utils.historical_data import HistoricalData


async def get_minute_candles():
    # show 1 minute candles for AAPL in 1 year period of time
    async with TinkoffInvestmentsRESTClient(
        token="TOKEN", environment=Environment.SANDBOX
    ) as client:
        historical_data = HistoricalData(client)
        async for candle in historical_data.iter_candles(
            figi="BBG000B9XRY4",
            dt_from=datetime(2019, 1, 1),
            dt_to=datetime(2020, 1, 1),
            interval=CandleResolution.MIN_1,
        ):
            print(candle)


asyncio.run(get_minute_candles())
```

TODO
--------------------------------------------------------------------------------

* allow to provide str constants along with specific enum objects
* add ability to unsubscribe by pattern
* rename some fields
* make some fields in snake case
* generate documentation
