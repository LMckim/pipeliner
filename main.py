import asyncio
import logging
import os

from dotenv import load_dotenv
import psycopg

from src import get_time_series_data, write_timeseries_to_excel, upload_symbol_data

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

    aconn = await psycopg.AsyncConnection.connect(
        host=os.environ["PG_HOST"],
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASS"],
        dbname=os.environ["PG_DBNAME"],
        port=os.environ["PG_PORT"],
    )

    await upload_symbol_data(aconn, data)


if __name__ == "__main__":
    asyncio.run(main())
