
from app.models.event import EventSlugHistory
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from utils.db_utils import save_changes_to_db, create_test_user, create_test_event, create_test_note, create_test_favorite
import pytest



def test_user_note_relationships(db_session):

    # test user creation
    user = create_test_user(db_session)

    assert user is not None

    # test user can create a note for the first historical event
    first_event = create_test_event(db_session)

    assert first_event is not None

    first_note = create_test_note(db_session, user=user, event=first_event)

    # test user-note-event relationships
    assert first_note is not None
    assert first_note.user_id == user.id
    assert first_note.event_id == first_event.id

    assert first_note.user == user
    assert first_note.event == first_event

    # test user can create a new note for the second historical event

    second_event = create_test_event(db_session, title=f'Stalin\'s Purges', year=1936, description='Great Terror began in 1937', country='Soviet Union', category='Totalitarianism')

    assert second_event is not None

    second_note = create_test_note(db_session, user=user, event=second_event)

    # test user-note-event relationships
    assert second_note is not None
    assert second_note.user_id == user.id
    assert second_note.event_id == second_event.id

    assert second_note.user == user
    assert second_note.event == second_event

    assert len(user.notes) == 2
    assert user.notes[0] == first_note
    assert user.notes[1] == second_note

def test_event_note_relationships(db_session):

    user = create_test_user(db_session)
    event = create_test_event(db_session)
    first_note = create_test_note(db_session, user=user, event=event)
    second_note = create_test_note(db_session, user=user, event=event)

    assert len(event.notes) == 2

    assert event.notes[0] == first_note
    assert event.notes[1] == second_note

    assert first_note.event == event
    assert second_note.event == event

def test_user_favorite_relationships(db_session):

    user = create_test_user(db_session)
    first_event = create_test_event(db_session)
    favorite = create_test_favorite(db_session, user=user, event=first_event)

    assert favorite is not None

    assert favorite.user_id == user.id
    assert favorite.event_id == first_event.id

    assert favorite.user == user
    assert favorite.event == first_event

    second_event = create_test_event(db_session, title='Cuba crisis', description='Cuba crisis happened in 1962', country='Cuba', category='Crisis', year=1962)

    favorite = create_test_favorite(db_session, user=user, event=second_event)

    assert favorite.user_id == user.id
    assert favorite.event_id == second_event.id

    assert favorite.user == user
    assert favorite.event == second_event

    assert len(user.favorites) == 2

def test_user_cannot_add_same_event_to_favorites_twice(db_session):

    user = create_test_user(db_session)
    event = create_test_event(db_session)
    favorite = create_test_favorite(db_session, user=user, event=event)

    assert favorite.user == user
    assert favorite.event == event

    assert len(user.favorites) == 1

    with pytest.raises(IntegrityError):
        create_test_favorite(db_session, user=user, event=event)

    db_session.rollback()

def test_event_favorite_relationships(db_session):

    first_user = create_test_user(db_session)
    second_user = create_test_user(db_session, email='new_user@example.com')

    event = create_test_event(db_session)

    create_test_favorite(db_session, user=first_user, event=event)
    create_test_favorite(db_session, user=second_user, event=event)

    assert first_user.favorites[0].event_id == event.id
    assert second_user.favorites[0].event_id == event.id


def test_user_event_relationships(db_session):

    user = create_test_user(db_session)

    first_event = create_test_event(db_session)
    second_event = create_test_event(db_session, title='French revolution', year=1889, description='French revolution', country='France')

    create_test_favorite(db_session, user=user, event=first_event)
    create_test_favorite(db_session, user=user, event=second_event)

    assert user.favorites[0].event == first_event
    assert user.favorites[1].event == second_event

    assert first_event.favorites[0].user == user
    assert second_event.favorites[0].user == user

    second_user = create_test_user(db_session, email='second_user@example.com')

    create_test_favorite(db_session, user=second_user, event=first_event)
    create_test_favorite(db_session, user=second_user, event=second_event)

    assert second_user.favorites[0].event == first_event
    assert second_user.favorites[1].event == second_event

    assert len(first_event.favorites) == 2
    assert len(second_event.favorites) == 2

    assert first_event.favorites[0].user == user
    assert first_event.favorites[1].user == second_user

    assert second_event.favorites[0].user == user
    assert second_event.favorites[1].user == second_user





def test_event_slug_relationships(db_session):

    # test event creation
    event = create_test_event(db_session)

    assert event is not None
    assert event.title == 'Russian revolution'
    assert 'russian-revolution' in event.slug

    event.title = 'Russian Civil War'
    save_changes_to_db(db_session)

    # test event slug generation
    assert 'russian-civil-war' in event.slug

    old_slug = db_session.scalar(select(EventSlugHistory).where(EventSlugHistory.event_id == event.id))

    assert old_slug is not None
    assert old_slug.event_id == event.id

    slug_history = list(db_session.scalars(select(EventSlugHistory).where(EventSlugHistory.event_id == event.id)))

    assert len(slug_history) > 0
    assert old_slug == slug_history[0]




