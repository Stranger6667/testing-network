import pytest
from pytest_factoryboy import register

from booking.app import create_app
from booking.models import db

from . import factories

register(factories.ExchangeRateFactory)


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture
def database(app):
    db.create_all()
    yield
    db.session.commit()
    db.drop_all()
