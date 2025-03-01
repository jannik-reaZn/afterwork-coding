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
        """
        Initialize the repository with the provided session and entity class.
        """
        self.session = session
        self.entity_cls = entity_cls

    def create(self, create_model: CreateModel):
        """
        Creates a new entity in the repository from the given create model.

        Args:
            create_model (CreateModel): The model containing the data to create the new entity.

        Returns:
            DomainModel: The created entity converted to its domain representation.
        """
        model: CreateModel = self.entity_cls.from_create_model(create_model)
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
        entity: Optional[SqlEntityModel] = self.session.get(self.entity_cls, id)
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
        """
        Converts a SQL entity model to a domain model.

        Args:
            entity (Optional[SqlEntityModel]): The SQL entity model to convert.

        Returns:
            Optional[DomainModel]: The converted domain model, or None if the input entity is None.
        """

        return entity.to_domain() if entity else None
