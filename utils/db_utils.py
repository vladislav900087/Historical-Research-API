from sqlalchemy.orm import Session
from app.models.user import User
from app.models.event import Event
from app.models.note import Note
from app.models.favorite import Favorite
from app.models.note import Note



def save_to_db(db_session: Session, model_instance) -> None:

    db_session.add(model_instance)
    db_session.commit()
    db_session.refresh(model_instance)

def save_changes_to_db(db_session: Session) -> None:

    db_session.commit()

def create_test_user(db_session: Session, email: str = 'test_user@example.com') -> User:

    user = User(email=email, hashed_password='hashed_password')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def create_test_event(db_session: Session, title: str = 'Russian revolution', description: str = 'Russian revolution happened on October 25, 1917', country: str = 'Russia', category: str = 'Revolutions', year: int = 1917) -> Event:


    event = Event(title=title, description=description, content='Content', year=year, country=country, category=category)

    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    return event

def create_test_note(db_session: Session, user: User | None = None, event: Event | None = None) -> Note:

    if user is None:
        user = create_test_user(db_session)
    if event is None:
        event = create_test_event(db_session)

    note = Note(user_id=user.id, event_id=event.id, content=' A user\'s content')

    db_session.add(note)
    db_session.commit()

    db_session.refresh(note)

    return note

def create_test_favorite(db_session: Session, user: User | None = None, event: Event | None = None) -> Favorite:

    if user is None:
        user = create_test_user(db_session)

    if event is None:
        event = create_test_event(db_session)

    favorite = Favorite(user_id=user.id, event_id=event.id)

    db_session.add(favorite)
    db_session.commit()
    db_session.refresh(favorite)

    return favorite




