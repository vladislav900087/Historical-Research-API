from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import String, DateTime, func
from app.db.base import Base
from datetime import datetime


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    notes: Mapped[list['Note']] = relationship('Note', back_populates='user', cascade='all, delete-orphan')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='user', cascade='all, delete-orphan')


