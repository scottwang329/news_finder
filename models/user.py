from db import db
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    username = db.Column(postgresql.VARCHAR, unique=True, nullable=False)
    password = db.Column(postgresql.VARCHAR, nullable=False)
    created_at = db.Column(postgresql.TIMESTAMP, nullable=False)

    def __init__(self, username, password):
        # Generate random uuid for each user
        self.id = uuid.uuid4()
        self.username = username
        self.password = password
        self.created_at = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
