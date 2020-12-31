from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Post, Tag, Comment

engine = create_engine('sqlite:///ot_blog.db', echo=True)
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
