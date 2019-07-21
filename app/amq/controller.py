import json
from os import getenv

import pika
from app.taiga import controller


def setup():
    URL = getenv('CLOUDAMQP_URL')
    return pika.URLParameters(URL)


def callback_project(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    controller.manage_project(body)


def callback_collaborator(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    controller.manage_collaborators(body)
