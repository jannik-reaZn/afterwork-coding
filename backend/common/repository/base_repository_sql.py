from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import Session, select

from backend.common.repository.entities.base_sql_entity import BaseSqlEntity
from backend.common.repository.query_builder import QueryBuilderSql
from backend.common.repository.types import FindWhereCondition

DomainModel = TypeVar("DomainModel", bound=BaseModel)
SqlEntityModel = TypeVar("SqlEntityModel", bound=BaseSqlEntity)
CreateModel = TypeVar("CreateModel", bound=BaseModel)


class BaseRepositorySql(Generic[SqlEntityModel]):
    """
    BaseRepositorySql provides a generic implementation for basic CRUD operations on SQL entities.

    This class can be extended by specific repository implementations to handle particular entities.

    Args:
        session (Session): The SQLAlchemy session used for database interactions.
        entity_class (Type[SqlEntityModel]): The class of the SQL entity being managed by the
        repository.
    """

    def __init__(self, session: Session, entity_class: Type[SqlEntityModel]):
        """
        Initialize the repository with the provided session and entity class.
        """
        self.session = session
        self.entity_class = entity_class

    def create(self, create_model: CreateModel):
        """
        Creates a new entity in the repository from the given create model.

        Args:
            create_model (CreateModel): The model containing the data to create the new entity.

        Returns:
            DomainModel: The created entity converted to its domain representation.
        """
        model: CreateModel = self.entity_class.from_create_model(create_model)
        entity: SqlEntityModel = self._create(model)
        return BaseRepositorySql.to_domain(entity)

    def get_by_id(self, id: int) -> Optional[DomainModel]:
        """
        Retrieve an entity by its unique identifier.

        Args:
            id (int): The unique identifier of the entity to retrieve.

        Returns:
            Optional[DomainModel]: The entity matching the provided identifier, or None if no entity
            was found.
        """
        entity: Optional[SqlEntityModel] = self._get_one_by(condition={"id": id})
        return BaseRepositorySql.to_domain(entity)

    def delete(self, id: int) -> None:
        """
        Delete an entity by its unique identifier.

        Args:
            id (int): The unique identifier of the entity to delete.
        """
        entity: Optional[SqlEntityModel] = self._get_one_by(condition={"id": id})
        if entity:
            self.session.delete(entity)

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

    def _get_one_by(self, condition: FindWhereCondition) -> Optional[SqlEntityModel]:
        """
        Retrieve a single entity from the database that matches the given condition.

        Args:
            condition (FindWhereCondition): The condition to filter the query.

        Returns:
            Optional[SqlEntityModel]: The entity that matches the condition, or None if no match is
            found.
        """
        statement = (
            QueryBuilderSql(entity_class=self.entity_class, statement=select(self.entity_class))
            .set_filter(condition)
            .get()
        )
        entity = self.session.exec(statement).first()
        return entity

    @staticmethod
    def to_domain(entity: Optional[SqlEntityModel]) -> Optional[DomainModel]:
        """
        Converts a SQL entity model to a domain model.

        Args:
            entity (Optional[SqlEntityModel]): The SQL entity model to convert.

        Returns:
            Optional[DomainModel]: The converted domain model, or None if the input entity is None.
        """

        return entity.to_domain() if entity else None
