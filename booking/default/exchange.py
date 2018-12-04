from decimal import Decimal

from ..exceptions import NoExchangeRateError
from ..models import ExchangeRate


def to_eur(amount: Decimal, currency: str):
    """Convert to EUR."""
    if currency == "EUR":
        return amount
    rate = ExchangeRate.query.filter_by(currency=currency).one_or_none()
    if not rate:
        raise NoExchangeRateError("No such rate")
    return amount / rate.ratio
