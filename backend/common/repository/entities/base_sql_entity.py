from datetime import datetime
from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel

from backend.common.utility import get_time_now


class BaseSqlEntity(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=lambda: get_time_now(), nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: get_time_now(),
        nullable=False,
        sa_column_info={"onupdate": get_time_now},
    )
