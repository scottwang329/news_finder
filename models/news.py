from db import db
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


class NewsModel(db.Model):
    __tablename__ = 'news'

    id = db.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    source = db.Column(postgresql.VARCHAR, nullable=False)
    author = db.Column(postgresql.VARCHAR)
    title = db.Column(postgresql.VARCHAR, nullable=False)
    description = db.Column(postgresql.VARCHAR)
    url = db.Column(postgresql.VARCHAR, nullable=False)
    urlToImage = db.Column(postgresql.VARCHAR)
    publishedAt = db.Column(postgresql.TIMESTAMP, nullable=False)
    content = db.Column(postgresql.TEXT)

    def __init__(self, **article):
        # Generate uuid based on url of the article
        self.id = uuid.uuid5(uuid.NAMESPACE_URL, article["url"])
        self.source = article["source"]['name']
        self.author = article["author"]
        self.title = article["title"]
        self.description = article["description"]
        self.url = article["url"]
        self.urlToImage = article["urlToImage"]
        self.publishedAt = article["publishedAt"]
        self.content = article["content"]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def bulk_save_to_db(cls, newsList):
        try:
            db.session.add_all(newsList)
            db.session.commit()
        except IntegrityError as err:
            if err.orig.pgcode != errorcodes.UNIQUE_VIOLATION:
                raise err
