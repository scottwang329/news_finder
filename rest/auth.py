from flask import (
    Blueprint, request, Response
)
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from exceptions.duplicate_user_exception import DuplicateUserException
from exceptions.invalid_request_exception import InvalidRequestException
from marshmallow import Schema, fields, ValidationError

bp = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


@bp.route('/register', methods=(['POST']))
def register():
    data = request.json
    try:
        RegisterSchema().load(data)
    except ValidationError as err:
        raise InvalidRequestException()
    if UserModel.find_by_username(data["username"]):
        raise DuplicateUserException()

    user = UserModel(**data)
    user.save_to_db()
    return {"message": "User created successfully."}, 201


@ bp.route('/login', methods=(['POST']))
def login():
    return Response(status=200)


@ bp.errorhandler(DuplicateUserException)
def handle_duplicate_user_exception(ex: Exception):
    return {"message": str(ex)}, 400


@ bp.errorhandler(InvalidRequestException)
def handle_duplicate_user_exception(ex: Exception):
    return {"message": str(ex)}, 400
