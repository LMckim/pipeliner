import asyncio
import json
import logging
import os
from typing import TypedDict

import aiohttp
from dotenv import load_dotenv

load_dotenv(override=True)

td_endpoint = "https://api.twelvedata.com"


class Meta(TypedDict):
    symbol: str
    interval: str
    currency: str
    exchange_timezone: str
    exchange: str
    mic_code: str
    type: str


class TimeSeriesValue(TypedDict):
    datetime: str
    open: str
    high: str
    low: str
    close: str
    volume: str


class TimeSeriesResponse(TypedDict):
    meta: Meta
    values: list[TimeSeriesValue]


async def main():
    key = os.environ["TWELVEDATA_KEY"]
    async with aiohttp.ClientSession(
        base_url=td_endpoint, headers={"Authorization": f"apikey {key}"}
    ) as sess:
        async with sess.get(
            "/time_series", params={"symbol": os.environ["SYMBOLS"], "interval": "1min"}
        ) as resp:
            if resp.status != 200:
                logging.warning(resp.status)
                logging.warning(await resp.content.read())
            else:
                data = json.loads(str(await resp.content.read(), encoding="utf8"))
                # single symbol
                if "meta" in data:
                    data: TimeSeriesResponse
                    meta = data["meta"]
                    symbol = meta["symbol"]
                    for row in data["values"]:
                        logging.info(symbol, row["datetime"], row["high"])
                else:
                    # multiple symbols
                    data: dict[str, TimeSeriesResponse]
                    for symbol, ticker_data in data.items():
                        meta = ticker_data["meta"]
                        symbol = meta["symbol"]
                        for row in ticker_data["values"]:
                            logging.info(symbol, row["datetime"], row["high"])


if __name__ == "__main__":
    asyncio.run(main())
