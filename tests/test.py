import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base, User, Post

engine = create_engine('sqlite:////home/alexandra/ot_blog/ot_blog_test.db')
Session = scoped_session(sessionmaker(bind=engine))


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


class TestBlogManager:
    def test_can_get_all_users(self, db_session):
        user1 = User(id=1, name='A', fullname='Alex', nickname='AA')
        user2 = User(id=2, name='J', fullname='John', nickname='JJ')
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()
        users = db_session.query(User).all()
        assert len(users) == 2

    def test_can_get_all_posts_of_user(self, db_session):
        user1 = User(id=1, name='A', fullname='Alex', nickname='AA')
        user2 = User(id=2, name='J', fullname='John', nickname='JJ')
        post1 = Post(id=1, text='This is my first post', user_id=user1.id)
        post2 = Post(id=2, text='This is my second post', user_id=user1.id)
        db_session.add(user1)
        db_session.add(user2)
        db_session.add(post1)
        db_session.add(post2)
        db_session.commit()
        user_posts = db_session.query(Post).filter_by(user_id=user1.id).all()
        assert len(user_posts) == 2
