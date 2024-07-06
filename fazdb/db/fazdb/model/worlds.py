from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from . import BaseModel

from sqlalchemy.dialects.mysql import VARCHAR, SMALLINT, DATETIME


class Worlds(BaseModel):
    __tablename__ = "worlds"

    name: Mapped[str] = mapped_column(VARCHAR(16), nullable=False, primary_key=True)
    player_count: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    time_created: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
