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
    if data['action'] == 'add':
        add_project(project_name, taiga_object)
    elif data['action'] == 'remove':
        remove_project(project_name, taiga_object)

    # TODO Enviar callback?


def remove_project(project_name, taiga_object):
    username = taiga_object.me().username
    project_slug = '{}-{}'.format(username, project_name.lower())
    project = taiga_object.projects.get_by_slug(project_slug)
    project.delete()
    print('{} removed succesfully!'.format(project_name))


def add_project(project_name, taiga_object):
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

    project.list_memberships().get()
    for collaborator in collaborators:
        if data['action'] == 'add':
            add_collaborator(project, role, collaborator)
        elif data['action'] == 'remove':
            remove_collaborator(project, role, collaborator, project_name)


def add_collaborator(project, role, collaborator):
    """
        Funcion responsable for adding collaborators to the project.
    """
    project.add_membership(email=collaborator, role=role.id, username=collaborator)
    print('{} added succesfully on {}!'.format(
        collaborator, project.name))


def remove_collaborator(project, role, collaborator, project_name):
    """
        Funcion responsable to remove collaborators from the project.
    """
    membership = project.list_memberships().get(email=collaborator, role=role.id)

    if membership is None:
        return print('{} doesn\'t exist in {}!'.format(collaborator, project))
    else:
        membership.delete()
        return print('{} removed succesfully from {}!'.format(collaborator, project_name))
