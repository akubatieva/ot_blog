from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker

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
Session = sessionmaker(bind=engine)
session = Session()
user1 = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
user2 = User(name='al', fullname='Alexandra K', nickname='alnickname')
post1 = Post(title='Cyberpunk 2077',
             text='Cyberpunk 2077 is a 2020 action role-playing video game developed and published by CD Projekt. '
                  'The story takes place in Night City, an open world set in the Cyberpunk universe.',
             user_id=user1.id,
             user=user1)
post2 = Post(title='Skyrim',
             text='The Elder Scrolls V: Skyrim is an open world action role-playing video game '
                  'developed by Bethesda Game Studios and published by Bethesda Softworks.',
             user_id=user2.id,
             user=user2)
tag1 = Tag(text='rpg', posts=[post1, post2])

comment1 = Comment(text='This is my comment about Cyberpunk 2077', user=user2, post=post1,
                   post_id=post1.id, user_id=user2.id)
comment2 = Comment(text='This is my comment about Skyrim', user_id=user1.id, user=user1,
                   post=post2, post_id=post2.id)
session.add_all([user1, user2, post1, post2, tag1, comment1, comment2])
session.commit()
# TODO: Есть пример запроса на выборку данных из базы (через ORM)
# TODO: change absolute paths for dbs to rel
