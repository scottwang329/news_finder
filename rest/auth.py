from flask import (
    Blueprint, request, Response
)
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=(['POST']))
def register():
    return {"message": "User created successfully."}, 201


@bp.route('/login', methods=(['POST']))
def login():
    return Response(status=200)
