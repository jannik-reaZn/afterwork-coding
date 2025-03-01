from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import Session

from backend.common.repository.entities.base_sql_entity import BaseSqlEntity

DomainModel = TypeVar("DomainModel", bound=BaseModel)
SqlEntityModel = TypeVar("SqlEntityModel", bound=BaseSqlEntity)
CreateModel = TypeVar("CreateModel", bound=BaseModel)


class BaseRepositorySql(Generic[SqlEntityModel]):
    """
    BaseRepositorySql provides a generic implementation for basic CRUD operations on SQL entities.

    This class can be extended by specific repository implementations to handle particular entities.

    Args:
        session (Session): The SQLAlchemy session used for database interactions.
        entity_cls (Type[SqlEntityModel]): The class of the SQL entity being managed by the
        repository.
    """

    def __init__(self, session: Session, entity_cls: Type[SqlEntityModel]):
        self.session = session
        self.entity_cls = entity_cls

    def create(self, create_model: CreateModel):
        model: CreateModel = self.entity_cls.from_create_model(create_model)
        entity: SqlEntityModel = self._create(model)
        return BaseRepositorySql.to_domain(entity)

    def _create(self, entity: SqlEntityModel) -> SqlEntityModel:
        """
        Create a new entity in the database.

        Args:
            entity (SqlEntityModel): The entity instance or a dictionary of attributes to create a
            new entity instance.

        Returns:
            SqlEntityModel: The created and persisted entity instance.
        """
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    @staticmethod
    def to_domain(entity: Optional[SqlEntityModel]) -> Optional[DomainModel]:
        return entity.to_domain() if entity else None
