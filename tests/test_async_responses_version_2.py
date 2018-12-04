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


@pytest.fixture
def setup_rates(aioresponses):
    def inner(**kwargs):
        aioresponses.get(re.compile(r"^http://127.0.0.1:5000/to_eur.*$"), **kwargs)

    return inner


async def test_save_transaction(setup_rates):
    setup_rates(payload={"result": "100"})
    transaction = await save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


async def test_save_transaction_no_rates(setup_rates):
    setup_rates(payload={"detail": "No such rate"}, status=400)
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        await save_transaction(1, Decimal(10), "NOK")
