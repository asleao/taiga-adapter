import json

from flask import (
    Blueprint
)
from flask import request
from taiga import TaigaAPI

blueprint = Blueprint('taiga', __name__)


def authenticate(request):
    data = request.json
    if 'token' in data:
        return TaigaAPI(token=data['token'])
    elif 'username' and 'password' in data:
        api = TaigaAPI()
        api.auth(data['username'], data['password'])
        return api.token


@blueprint.route('/v1/authorization', methods=['POST'])
def login():
    return json.dumps(authenticate(request))
