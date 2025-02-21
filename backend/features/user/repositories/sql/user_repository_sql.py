from backend.common.repository.base_repository_sql import BaseRepositorySql
from backend.database import SessionDep
from backend.features.user.repositories.sql.entities.user_entity import UserSqlEntity


class UserRepositorySql(BaseRepositorySql[UserSqlEntity]):
    def __init__(self, session: SessionDep):
        super().__init__(session=session, entity_cls=UserSqlEntity)

    def create_user(self, user: UserSqlEntity) -> UserSqlEntity:
        return self.create(entity=user)
