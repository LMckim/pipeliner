import logging

from psycopg import AsyncConnection
from psycopg.sql import SQL, Identifier

from src.twelvedata import TimeSeriesData


async def upload_symbol_data(
    aconn: AsyncConnection, data: dict[str, list[TimeSeriesData]], schema: str = "public"
):
    async with aconn.cursor() as acsr:
        for symbol, ticker_data in data.items():
            try:
                await acsr.execute(
                    SQL(
                        """
                    CREATE TABLE IF NOT EXISTS {schema}.{ticker_table} (
                        rec_id SERIAL,
                        timestamp TIMESTAMP WITHOUT TIME ZONE,
                        price NUMERIC(30,18)
                    )
                """
                    ).format(
                        schema=Identifier(schema),
                        ticker_table=Identifier(f"{symbol}_data"),
                    )
                )
            except Exception as e:
                logging.exception(e)
                await aconn.rollback()
            else:
                await aconn.commit()

            vals = []
            for row in ticker_data:
                vals.append((row.timestamp, row.price))

            try:
                await acsr.executemany(
                    SQL("""
                    INSERT INTO {schema}.{ticker_table} (
                        timestamp,
                        price
                    ) VALUES (%s, %s)
                """).format(
                        schema=Identifier(schema),
                        ticker_table=Identifier(f"{symbol}_data"),
                    ),
                    vals,
                )
            except Exception as e:
                logging.exception(e)
                await aconn.rollback()
            else:
                await aconn.commit()
