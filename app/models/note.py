from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, DateTime, func, Text
from app.db.base import Base
from datetime import datetime


class Note(Base):

    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user: Mapped['User'] = relationship('User', back_populates='notes')
    event: Mapped['Event'] = relationship('Event', back_populates='notes')




