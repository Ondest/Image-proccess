from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Image(Base):
    __tablename__ = "images"

    file_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(server_default=func.now())
    resolution: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
