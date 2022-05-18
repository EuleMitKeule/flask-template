from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from src.models import User
from src.common import ma, guard, api


class LoginQuerySchema(ma.Schema):
    username: str = ma.Str(required=True)
    password: str = ma.Str(required=True)


bp: Blueprint = Blueprint(
    "auth",
    "auth",
    url_prefix="/auth"
)


@bp.route("/login")
class AuthView(MethodView):

    @bp.response(200, User.Schema())
    @bp.arguments(LoginQuerySchema, location="query")
    def post(self, args: dict):
        username: str = args.get("username")
        password: str = args.get("password")

        user: User = guard.authenticate(username=username, password=password)
        jwt: str = guard.encode_jwt_token(user)

        user.update(access_token=jwt)
        
        user_dict: dict = User.dump(user)
        return jsonify(user_dict)


api.register_blueprint(bp)
