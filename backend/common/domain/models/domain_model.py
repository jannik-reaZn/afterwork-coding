from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DomainModel(BaseModel):
    """
    This class provides a common configuration for all domain models in the application.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
