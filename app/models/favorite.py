from sqlalchemy import ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from app.db.base import Base


class Favorite(Base):

    __tablename__ = 'favorites'

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_user_favorite_event'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped['User'] = relationship('User', back_populates='favorites')
    event: Mapped['Event'] = relationship('Event', back_populates='favorites')