from utils.db_utils import create_test_user
from app.models.user import User

def test_step_1_create_user(db_session):

    user = create_test_user(db_session)

    assert db_session.query(User).filter_by(email=user.email).first() is not None

def test_step_2_verify_db_is_empty_again(db_session):

    user = db_session.query(User).filter_by(email='test_user@example.com').first()

    assert user is None