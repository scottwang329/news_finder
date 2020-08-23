from db import db
from sqlalchemy.dialects import postgresql


class RecommendModel (db.Model):
    __tablename__ = 'recommend'

    user_id = db.Column(postgresql.UUID, primary_key=True)
    news_ids = db.Column(postgresql.ARRAY(postgresql.VARCHAR))

    @ classmethod
    def recommend_news_by_user_id(cls, user_id):
        news_ids = cls.query.filter_by(user_id=user_id).first().news_ids
        return [] if news_ids is None else news_ids
