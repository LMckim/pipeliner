import aiohttp
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import json
import logging
from typing import TypedDict


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


@dataclass
class TimeSeriesData:
    symbol: str
    timestamp: datetime
    price: Decimal


def parse_values(symbol: str, rows: list[dict]):
    ts_data: list[TimeSeriesData] = []
    for row in rows:
        logging.info(f"{symbol}, {row['datetime']}, {row['high']}")
        ts_data.append(
            TimeSeriesData(
                symbol,
                datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S"),
                Decimal(row["high"]),
            )
        )
    return ts_data


async def get_time_series_data(endpoint: str, api_key: str, symbols: list[str]):
    ts_data: dict[str, list[TimeSeriesData]] = {}

    async with aiohttp.ClientSession(
        base_url=endpoint, headers={"Authorization": f"apikey {api_key}"}
    ) as sess:
        async with sess.get(
            "/time_series", params={"symbol": ",".join(symbols), "interval": "1min"}
        ) as resp:
            if resp.status != 200:
                logging.warning(resp.status)
                logging.warning(await resp.content.read())
            else:
                data = json.loads(str(await resp.content.read(), encoding="utf8"))
                # single symbol
                if "meta" in data:
                    data: TimeSeriesResponse  # type: ignore
                    meta = data["meta"]
                    symbol = meta["symbol"]
                    ts_data[symbol] = parse_values(symbol, data["values"])

                else:
                    # multiple symbols
                    data: dict[str, TimeSeriesResponse]  # type: ignore
                    for symbol, ticker_data in data.items():
                        meta = ticker_data["meta"]
                        symbol = meta["symbol"]
                        ts_data[symbol] = parse_values(symbol, ticker_data["values"])

    return ts_data
