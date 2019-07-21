from taiga import TaigaAPI
from taiga.models import Memberships, Membership

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
    project = taiga_object.projects.create(project_name, project_name, is_private=False)
    project.add_role('Desenvolvedor', permissions=["add_issue", "modify_issue"])

    print('{} created succesfully!'.format(project_name))

    # TODO Enviar callback?


def manage_collaborators(data):
    """
        Funcion responsable for manage collaborators of the project.
    """
    taiga_object = authenticate(data=data)
    collaborators = data['collaborators']
    project_name = data['name']
    username = taiga_object.me().username
    project_slug = '{}-{}'.format(username, project_name.lower())
    project = taiga_object.projects.get_by_slug(project_slug)
    role = project.list_roles().get(name='Desenvolvedor')

    for collaborator in collaborators:
        if data['action'] == 'add':
            add_collaborator(project, role, collaborator, username)
        elif data['action'] == 'remove':
            remove_collaborator(project, collaborator, project_name)


def add_collaborator(project, role, collaborator, username):
    """
        Funcion responsable for adding collaborators to the repository.
    """

    project.add_membership(collaborator, role.id, username=username)
    print('{} added succesfully on {}!'.format(
        collaborator, project.name))


def remove_collaborator(project, collaborator, project_name):
    """
        Funcion responsable to remove collaborators from the repository.
    """
    if project.has_in_collaborators(collaborator) == False:
        # TODO: realizar um retorno http para usuário não existente
        return print('{} doesn\'t exist in {}!'.format(collaborator, project_name))
    else:
        project.remove_from_collaborators(collaborator)
        return print('{} removed succesfully from {}!'.format(collaborator, project_name))
