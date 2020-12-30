from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:////home/alexandra/ot_blog/ot_blog.db', echo=True)
Base = declarative_base()

post_tags = Table('post_tags', Base.metadata,
                  Column('post_id', ForeignKey('posts.id'), primary_key=True),
                  Column('tag_id', ForeignKey('tags.id'), primary_key=True))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    fullname = Column(String, nullable=True)
    nickname = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')>"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref="posts")
    tags = relationship('Tag', secondary=post_tags, back_populates='posts')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="comments")
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", backref="comments")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    posts = relationship('Post', secondary=post_tags, back_populates='tags')


Base.metadata.create_all(bind=engine)
