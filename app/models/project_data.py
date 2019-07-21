"""
    Class to store information, that came from the amq,
    about the repository.
"""
from typing import List


class ProjectData:
    collaborators: List[str]

    def __init__(self, repository_name, action, token, language) -> None:
        super().__init__()
        self.repository_name = repository_name
        self.action = action
        self.token = token
        self.language = language