from db import db
from sqlalchemy.dialects import postgresql
import uuid
from sqlalchemy import ForeignKey
from datetime import datetime


class RatingModel(db.Model):
    __tablename__ = 'rating'

    id = db.Column(postgresql.UUID, primary_key=True)
    user_id = db.Column(postgresql.UUID, ForeignKey(
        'users.id'), nullable=False)
    news_id = db.Column(postgresql.UUID, ForeignKey('news.id'), nullable=False)
    rating = db.Column(postgresql.SMALLINT, nullable=False)
    date = db.Column(postgresql.TIMESTAMP, nullable=False)

    def __init__(self, ser_id, news_id, rating):
        # Generate random uuid for each user
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.news_id = news_id
        self.rating = rating
        self.date = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
