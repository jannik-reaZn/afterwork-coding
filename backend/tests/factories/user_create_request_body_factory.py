import factory

from backend.features.user.repositories.sql.entities import UserSqlEntity
from backend.features.user.routes.requests import UserCreateRequestBody


class UserCreateRequestBodyFactory(factory.Factory[UserCreateRequestBody]):
    class Meta(factory.Factory.Meta):
        model = UserCreateRequestBody

    id = factory.Sequence(lambda n: int(n))  # type: ignore[arg-type]
    username = factory.Faker("name")
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    hashed_password = UserSqlEntity.hash_password(str(factory.Faker("password")))
