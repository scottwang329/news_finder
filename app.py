from flask import Flask
from flask_jwt_extended import JWTManager
from rest import auth, news
from marshmallow import ValidationError
from db import db
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from recommend.collabrative_filtering import generate_recommend_table

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
    JWT_SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost:5432/news_finder',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# app.config["SQLALCHEMY_DATABASE_URL"] = 'postgresql://postgres:postgres@localhost:5432/news_finder'

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# # ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass

jwt = JWTManager(app)

app.register_blueprint(auth.bp)
app.register_blueprint(news.bp)

# @jwt.user_claims_loader
# def add_claims_to_jwt(identity):

db.init_app(app)
ctx = app.app_context()
app.app_context().push()
db.create_all()

generate_recommend_table(ctx)

scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: generate_recommend_table(ctx),
                  trigger="interval", minutes=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))


@ app.errorhandler(ValidationError)
def handle_duplicate_user_exception(ex: Exception):
    return {"message": str(ex)}, 400


if __name__ == '__main__':

    app.run(port=5000, debug=True)
