from flask import (
    Blueprint, request, Response
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from exceptions import *
from marshmallow import Schema, fields, ValidationError

bp = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


@bp.route('/register', methods=(['POST']))
def register():
    data = request.json
    # Validate request body
    RegisterSchema().load(data)

    if UserModel.find_by_username(data["username"]):
        raise DuplicateUserException()

    data["password"] = generate_password_hash(data["password"])

    user = UserModel(**data)
    user.save_to_db()
    return {"message": "User created successfully."}, 201


@ bp.route('/login', methods=(['POST']))
def login():
    data = request.json
    # Validate request body
    LoginSchema().load(data)

    # find user in database
    user = UserModel.find_by_username(data['username'])
    if user == None or not check_password_hash(user.password, data["password"]):
        raise InvalidCredentialException()
    access_token = create_access_token(identity=user.id)
    return {
        "access_token": access_token
    }, 200


@ bp.errorhandler(DuplicateUserException)
def handle_duplicate_user_exception(ex: Exception):
    return {"message": str(ex)}, 400


@ bp.errorhandler(InvalidCredentialException)
def handle_invalid_credential_exception(ex: Exception):
    return {"message": str(ex)}, 401
