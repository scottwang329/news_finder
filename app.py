from flask import Flask
from flask_jwt_extended import JWTManager
from rest import auth
from db import db

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

# @jwt.user_claims_loader
# def add_claims_to_jwt(identity):


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
