from backend.features.user.repositories.sql.entities.user_entity import User
from backend.features.user.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: User) -> User:
        return self.user_repo.create_user(user)
