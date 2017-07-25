from flask import session
from src.common.database import Database
import uuid
import datetime

from src.models.blog import Blog


class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex() if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})

        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # user.login_valid("eddie@flaskcasts.com", "password")
        # Check whether a users email/password combo is correct.
        user = User.get_by_email(email)

        if user is not None:
            # check the password
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        # if user exists, fail
        # if not create user
        user = cls.get_by_email(email)
        if user is None:
            # the user does not exist so create.
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # user already exists.
            return False
        pass

    @staticmethod
    def login(user_email):
        # login_valid has already been called.
        # store the email in a session
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password  # NOT SAFE TO SEND OVER NETWORK
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())