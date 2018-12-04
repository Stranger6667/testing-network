from decimal import Decimal
import re

from aioresponses import aioresponses as _aioresponses
import pytest

from booking.aio.payments import save_transaction
from booking.exceptions import NoExchangeRateError

pytestmark = [pytest.mark.usefixtures("database"), pytest.mark.asyncio]


@pytest.fixture
def aioresponses():
    with _aioresponses() as mock:
        yield mock


async def test_save_transaction(aioresponses):
    aioresponses.get(re.compile(r"^http://127.0.0.1:5000/to_eur.*$"), payload={"result": "100"})
    transaction = await save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


async def test_save_transaction_no_rates(aioresponses):
    aioresponses.get(re.compile(r"^http://127.0.0.1:5000/to_eur.*$"), payload={"detail": "No such rate"}, status=400)
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        await save_transaction(1, Decimal(10), "NOK")
