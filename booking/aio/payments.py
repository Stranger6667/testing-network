from decimal import Decimal

from . import exchange
from ..models import db, Transaction


async def save_transaction(booking_id: int, amount: Decimal, currency: str):
    """We need to store EUR amount as well."""
    amount_eur = await exchange.to_eur(amount, currency)

    transaction = Transaction(booking_id=booking_id, amount=amount, currency=currency, amount_eur=amount_eur)
    db.session.add(transaction)
    db.session.commit()
    return transaction
