from typing import Type, TypeVar

from sqlmodel import Session

from backend.common.repository.entities.base_sql_entity import BaseSqlEntity

SqlEntityModel = TypeVar("SqlEntityModel", bound=BaseSqlEntity)


class BaseRepositorySql:
    def __init__(self, session: Session, entity_cls: Type[SqlEntityModel]):
        self.session = session
        self.entity_cls = entity_cls
