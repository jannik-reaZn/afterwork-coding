import factory
from factory.alchemy import SQLAlchemyModelFactory

from backend.features.user.repositories.sql.entities.user_entity import User
from backend.tests.conftest import TestingSessionLocal


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_factory = TestingSessionLocal
        sqlalchemy_session_persistence = "commit"

    username = factory.Faker("name")
    email = factory.Faker("email")
    hashed_password = factory.LazyFunction(
        lambda: User.hash_password(str(factory.Faker("password")))
    )
