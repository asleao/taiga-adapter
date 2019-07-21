from taiga import TaigaAPI

from app.taiga.blueprint import authenticate


def authenticate(data):
    if 'token' in data:
        return TaigaAPI(token=data['token'])
    elif 'username' and 'password' in data:
        api = TaigaAPI()
        api.auth(data['username'], data['password'])
        return api.token


def manage_project(data):
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    taiga_object = authenticate(data)
    project_name = data['name']
    projeto = taiga_object.projects.create(project_name, project_name, is_private=False)
    print('{} created succesfully!'.format(project_name))

    # TODO Enviar callback?


def manage_collaborators(data):
    """
        Funcion responsable for manage collaborators of the project.
    """
