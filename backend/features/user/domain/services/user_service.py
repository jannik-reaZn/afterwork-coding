from fastapi import Depends

from backend.features.user.repositories.sql.entities.user_entity import UserSqlEntity
from backend.features.user.repositories.sql.user_repository_sql import UserRepositorySql
from backend.features.user.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepositorySql)):
        self.user_repo = user_repo

    def create_user(self, user: UserSqlEntity) -> UserSqlEntity:
        return self.user_repo.create(user)
