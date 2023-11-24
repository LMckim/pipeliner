import asyncio
import logging
import os

from dotenv import load_dotenv

from src import get_time_series_data, write_timeseries_to_excel

load_dotenv(override=True)
logging.getLogger().setLevel(logging.INFO)


ENDPOINT = "https://api.twelvedata.com"


async def main():
    key = os.environ["TWELVEDATA_KEY"]
    symbols = os.environ["SYMBOLS"].split(",")
    data = await get_time_series_data(
        ENDPOINT,
        key,
        symbols,
    )
    write_timeseries_to_excel("output.xlsx", data)


if __name__ == "__main__":
    asyncio.run(main())
