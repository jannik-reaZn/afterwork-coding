from backend.common.route.requests import RequestModel
from backend.features.user.domain.models import UserCreate
from backend.features.user.routes.requests.user_create_request_body import UserCreateRequestBody


class UserCreateRequest(RequestModel):
    user_create: UserCreateRequestBody

    def to_create_model(self) -> UserCreate:
        return self.user_create.to_create_model()
