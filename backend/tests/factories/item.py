import factory
from factory.alchemy import SQLAlchemyModelFactory

from backend.db import Item
from backend.tests.conftest import TestingSessionLocal


class ItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session_factory = TestingSessionLocal
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    is_available = factory.Faker("boolean")
