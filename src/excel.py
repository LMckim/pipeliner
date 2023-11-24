import logging

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from src.twelvedata import TimeSeriesData


def populate_sheet(sheet: Worksheet, symbol_data: list[TimeSeriesData]) -> None:
    sheet.append(["Price", "DateTime", "Price"])
    for row in symbol_data:
        sheet.append(
            [
                row.symbol,
                row.timestamp,
                row.price,
            ]
        )


def write_timeseries_to_excel(
    output_file: str, data: dict[str, TimeSeriesData]
) -> None:
    xl = openpyxl.Workbook()
    for symbol in data.keys():
        logging.info(f"Writing XL Sheet {symbol}")
        xl.create_sheet(symbol.upper())
        populate_sheet(xl[symbol.upper()], data[symbol])

    del xl["Sheet"]  # remove default worksheet
    xl.save(output_file)
