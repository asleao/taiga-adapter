import json
from os import getenv

import pika
from app.taiga import controller
from app.models.project_data import ProjectData


def setup():
    URL = getenv('CLOUDAMQP_URL')
    return pika.URLParameters(URL)


def callback_project(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    repository_data = ProjectData(body['name'],
                                  body['action'],
                                  body['token'],
                                  body['language'])
    controller.manage_project(repository_data)


def callback_collaborator(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    collaborator_data = ProjectData(body['name'],
                                    body['action'],
                                    body['token'],
                                    body['language'])
    collaborator_data.collaborators = body['collaborators']
    controller.manage_collaborators(collaborator_data)
