from db import db
from sqlalchemy.dialects import postgresql
import uuid
from sqlalchemy import ForeignKey
from datetime import datetime
from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import insert


class RatingModel(db.Model):
    __tablename__ = 'rating'

    id = db.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(postgresql.UUID, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    news_id = db.Column(postgresql.UUID, ForeignKey(
        'news.id', ondelete="CASCADE"), nullable=False)
    rating = db.Column(postgresql.SMALLINT, nullable=False)
    date = db.Column(postgresql.TIMESTAMP, nullable=False)
    __table_args__ = (
        db.UniqueConstraint("user_id", "news_id"),
    )

    def __init__(self, user_id, news_id, rating):
        # Generate random uuid for each user
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.news_id = news_id
        self.rating = rating
        self.date = datetime.now()

    def save_to_db(self):
        insert_stmt = insert(RatingModel).values(**self.asdict()).on_conflict_do_update(
            index_elements=['user_id', 'news_id'],
            set_=self.asdict()
        )
        db.session.execute(insert_stmt)
        db.session.commit()

    def asdict(self):
        return RatingSchema().dump(self)


class RatingSchema(Schema):
    id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    news_id = fields.Str(required=True)
    rating = fields.Int(required=True)
    date = fields.DateTime(required=True)
