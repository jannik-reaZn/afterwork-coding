from typing import Any, Generic, Self, Type, TypeVar

from sqlalchemy import Select

from backend.common.repository.entities.base_sql_entity import BaseSqlEntity
from backend.common.repository.query_builder_base import QueryBuilderBase

SqlModel = TypeVar("SqlModel", bound=BaseSqlEntity)


class QueryBuilderSql(Generic[SqlModel], QueryBuilderBase):
    def __init__(self, entity_class: Type[SqlModel], statement: Select[Any]):
        self._statement = statement
        self._entity_class = entity_class

    def set_filter(self, filter_params: dict[str, Any]) -> Self:
        for key, value in filter_params.items():
            if type(value) is list:
                self._statement = self._statement.filter(
                    getattr(self._entity_class, key).in_(value)
                )
            else:
                self._statement = self._statement.filter(getattr(self._entity_class, key) == value)

        return self

    def get(self) -> Select[Any]:
        return self._statement
