from db import db
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow import Schema, fields


class NewsModel(db.Model):
    __tablename__ = 'news'

    id = db.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    source = db.Column(postgresql.VARCHAR, nullable=False)
    author = db.Column(postgresql.VARCHAR)
    title = db.Column(postgresql.VARCHAR, nullable=False)
    description = db.Column(postgresql.VARCHAR)
    url = db.Column(postgresql.VARCHAR, unique=True, nullable=False)
    urlToImage = db.Column(postgresql.VARCHAR)
    publishedAt = db.Column(postgresql.TIMESTAMP, nullable=False)
    content = db.Column(postgresql.TEXT)

    def __init__(self, **article):
        # Generate uuid based on url of the article
        # self.id = uuid.uuid5(uuid.NAMESPACE_URL, article["url"])
        self.id = uuid.uuid4()
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

    def asdict(self):
        NewsSchema().dump(self)

    @classmethod
    def bulk_save_to_db(cls, newsList):
        insert_stmt = postgresql.insert(cls).values(
            NewsSchema(many=True).dump(newsList))
        update_dict = {x.name: x for x in insert_stmt.excluded}
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['url'],
            set_=update_dict
        )
        db.session.execute(upsert_stmt)
        db.session.commit()


class NewsSchema(Schema):
    id = fields.Str(required=True)
    source = fields.Str(required=True)
    author = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str()
    url = fields.Str(required=True)
    urlToImage = fields.Str()
    publishedAt = fields.Str(required=True)
    content = fields.Str()
