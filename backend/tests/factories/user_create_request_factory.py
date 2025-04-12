import factory

from backend.features.user.routes.requests import UserCreateRequest
from backend.tests.factories import UserCreateRequestBodyFactory


class UserCreateRequestFactory(factory.Factory[UserCreateRequest]):
    class Meta(factory.Factory.Meta):
        model = UserCreateRequest

    user_create = factory.SubFactory(UserCreateRequestBodyFactory)
