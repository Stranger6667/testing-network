from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Transaction(db.Model):
    """Payment transaction."""

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    booking_id = db.Column(db.Integer, nullable=False)

    amount = db.Column(db.Numeric, nullable=False)
    currency = db.Column(db.String(3), nullable=False)

    amount_eur = db.Column(db.Numeric, nullable=False)


class ExchangeRate(db.Model):
    """Current ratios to EUR."""

    currency = db.Column(db.String(3), primary_key=True)
    ratio = db.Column(db.Numeric, nullable=False)
