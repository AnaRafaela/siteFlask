from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker

from . import db
from .models import User, Post

def users(count=20):
    fake = Faker()
    i = 0
    while i < count:
        u = User(
            email=fake.email(),
            username=fake.user_name(),
            password='123',
            name=fake.name(),
            about_me=fake.text()
        )
        db.session.add(u)
        try:
            db.session.commit()
            i+=1
        except IntegrityError:
            db.session.rollback()

def posts(count=200):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(
            body=fake.text(),
            timestamp=fake.past_date(),
            author=u
        )
        db.session.add(p)
    db.session.commit()
