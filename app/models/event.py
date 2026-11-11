from sqlalchemy import String, event, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, mapped_column, Mapped, attributes
from app.db.base import Base
from slugify import slugify
from datetime import datetime
import uuid


class Event(Base):

    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    slug_history: Mapped[list['EventSlugHistory']] = relationship('EventSlugHistory', back_populates='event', cascade='all, delete-orphan')
    notes: Mapped[list['Note']] = relationship('Note', back_populates='event', cascade='all, delete-orphan')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='event', cascade='all, delete-orphan')





class EventSlugHistory(Base):

    __tablename__ = 'event_slug_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    old_slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    event: Mapped['Event'] = relationship('Event', back_populates='slug_history')




# lifecycle event listener
@event.listens_for(Event, 'before_insert')
def generate_slug(mapper, connection, target):
    if target.title and not target.slug:
        base_slug = slugify(target.title)
        target.slug = f'{base_slug}-{uuid.uuid4().hex[:8]}'

@event.listens_for(Event, 'before_update')
def update_slug_and_archive_old(mapper, connection, target):

    # updates the slug if the title is changed
    hist = attributes.get_history(target, 'title')
    if hist.has_changes():
        old_slug_value = target.slug

        base_slug = slugify(target.title)
        new_slug_value = f'{base_slug}-{uuid.uuid4().hex[:8]}'

        if old_slug_value != new_slug_value:

            connection.execute(EventSlugHistory.__table__.insert().values(old_slug=old_slug_value, event_id=target.id))

            target.slug = new_slug_value







