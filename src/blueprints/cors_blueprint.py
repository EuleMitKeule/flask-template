

from flask import Blueprint, Response, request

from const import ALLOWED_ORIGINS


bp: Blueprint = Blueprint("cors", __name__)

@bp.before_app_request
def check_origin():
    origin: str = request.headers.get("Origin")
    response: Response = Response()

    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
