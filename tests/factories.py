from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from booking import models
from booking.models import db

session = db.create_scoped_session()


class ExchangeRateFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ExchangeRate
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    currency = Faker("pystr", min_chars=3, max_chars=3)
    ratio = Faker("pydecimal", positive=True)
