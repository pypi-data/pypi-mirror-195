from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.models.project import Project

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client


_logger = logging.getLogger(__name__)


class Workspace:
    """Represent a Vectice Workspace.

    Workspaces are containers used to organize projects, assets, and
    users.

    Vectice users have access to a personal workspace and other
    workspaces so they can learn and collaborate with other users. An
    organization will have many workspaces, each with an Admin and
    Members with different privileges.

    Note that only an Org Admin can create a new workspace in the
    organization.

    You can get a workspace from your [`Connection`][vectice.Connection]
    object by calling `workspace()`:

    ```python
    import vectice

    connection = vectice.connect(...)
    my_workspace = connection.workspace("Iris workspace")
    ```

    Or you can get it directly when connecting to Vectice:

    ```python
    import vectice

    my_workspace = vectice.connect(..., workspace="Iris workspace")
    ```

    See [`Connection.connect`][vectice.Connection.connect] to learn
    how to connect to Vectice.
    """

    def __init__(self, id: int, name: str, description: str | None = None):
        """Initialize a workspace.

        Vectice users shouldn't need to instantiate Workspaces manually,
        but here are the workspace parameters.

        Parameters:
            id: The workspace identifier.
            name: The name of the workspace.
            description: The description of the workspace.
        """
        self._id = id
        self._name = name
        self._description = description
        self._client: Client
        self._connection: Connection

    def __post_init__(self, client: Client, connection: Connection):
        self._client = client
        self._connection = connection

    def __eq__(self, other: object):
        if not isinstance(other, Workspace):
            return NotImplemented
        return self.id == other.id

    def __repr__(self):
        return f"Workspace(name={self.name}, id={self._id}, description={self.description})"

    @property
    def id(self) -> int:
        """The workspace's id.

        Returns:
            The workspace's id.
        """
        return self._id

    @property
    def name(self) -> str:
        """The workspace's name.

        Returns:
            The workspace's name.
        """
        return self._name

    @property
    def description(self) -> str | None:
        """The workspace's description.

        Returns:
            The workspace's description.
        """
        return self._description

    @property
    def properties(self) -> dict:
        """The workspace's name and id.

        Returns:
            A dictionary containing the `name` and `id` items.
        """
        return {"name": self.name, "id": self.id}

    def project(self, project: str | int) -> Project:
        """Get a project.

        Parameters:
            project: The project name or id.

        Returns:
            The project.
        """
        item = self._client.get_project(project, self.id)
        _logger.info(f"Your current project: {item.id}")
        project_object = Project(item.id, self, item.name, item.description)
        return project_object

    @property
    def projects(self) -> list[Project]:
        """List projects.

        Returns:
            A list of projects in this workspace.
        """
        response = self._client.list_projects(self.id)
        return [Project(item.id, self, item.name, item.description) for item in response.list]

    @property
    def connection(self) -> Connection:
        """The Connection to which this workspace belongs.

        Returns:
            The Connection to which this workspace belongs.
        """
        return self._connection
