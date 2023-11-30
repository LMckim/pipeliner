from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from src import populate_sheet, TimeSeriesData


def test_populate_sheet():
    mock_sheet = []
    mock_data = [
        TimeSeriesData("TEST", datetime(2023, 2, 22, 1, 1, 0), Decimal("10.1")),
        TimeSeriesData("TEST", datetime(2023, 2, 22, 1, 2, 0), Decimal("10.2")),
        TimeSeriesData("TEST", datetime(2023, 2, 22, 1, 3, 0), Decimal("10.3")),
        TimeSeriesData("TEST", datetime(2023, 2, 22, 1, 4, 0), Decimal("10.4")),
    ]
    populate_sheet(mock_sheet, mock_data)
    assert mock_sheet[0] == ["Price", "DateTime", "Price"]
    for i, row in enumerate(mock_data):
        assert mock_sheet[i + 1] == [row.symbol, row.timestamp, row.price]
