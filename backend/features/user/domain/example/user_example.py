from backend.features.user.domain.models import User

USER_EXAMPLE = User(
    id=1,
    username="John",
    full_name="John Doe",
    email="john.doe@example.com",
    hashed_password="test_password",
)
