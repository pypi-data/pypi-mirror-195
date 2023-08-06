from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.models.datasource.datawrapper import DataWrapper
from vectice.models.phase import Phase
from vectice.utils.deprecation import DeprecationError

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.models import Workspace


_logger = logging.getLogger(__name__)


class Project:
    """Represent a Vectice project.

    A project reflects a typical Data Science project, including
    phases and the associated assets like code, datasets, models, and
    documentation. Multiple projects may be defined within each workspace.

    You can get a project from your [`Workspace`][vectice.models.Workspace]
    object by calling `project()`:

    ```python
    import vectice

    connection = vectice.connect(...)
    my_workspace = connection.workspace("Iris workspace")
    my_project = my_workspace.project("Iris project")
    ```

    Or you can get it directly when connecting to Vectice:

    ```python
    import vectice

    my_project = vectice.connect(..., workspace="Iris workspace", project="Iris project")
    ```

    See [`Connection.connect`][vectice.Connection.connect] to learn
    how to connect to Vectice.
    """

    __slots__ = ["_id", "_workspace", "_name", "_description", "_phase", "_client", "_pointers"]

    def __init__(
        self,
        id: int,
        workspace: Workspace,
        name: str,
        description: str | None = None,
    ):
        """Initialize a project.

        Vectice users shouldn't need to instantiate Projects manually,
        but here are the project parameters.

        Parameters:
            id: The project identifier.
            workspace: The workspace this project belongs to.
            name: The name of the project.
            description: A brief description of the project.
        """
        self._id = id
        self._workspace = workspace
        self._name = name
        self._description = description
        self._phase: Phase | None = None
        self._client = workspace._client

    def __repr__(self):
        return (
            f"Project(name='{self.name}', id={self._id}, description='{self.description}', workspace={self._workspace})"
        )

    def __eq__(self, other: object):
        if not isinstance(other, Project):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """The project's id.

        Returns:
            The project's id.
        """
        return self._id

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this project belongs.

        Returns:
            The workspace to which this project belongs.
        """
        return self._workspace

    @property
    def connection(self) -> Connection:
        """The Connection to which this project belongs.

        Returns:
            The Connection to which this project belongs.
        """
        return self._workspace.connection

    @property
    def name(self) -> str:
        """The project's name.

        Returns:
            The project's name.
        """
        return self._name

    @property
    def description(self) -> str | None:
        """The project's description.

        Returns:
            The project's description.
        """
        return self._description

    @property
    def properties(self) -> dict:
        """The project's identifiers.

        Returns:
            A dictionary containing the `name`, `id` and `workspace` items.
        """
        return {"name": self.name, "id": self.id, "workspace": self.workspace.id}

    @property
    def origin_dataset(self) -> None:
        """Deprecated. Use steps' [`origin_dataset`][vectice.models.Step.origin_dataset] instead.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Origin datasets are now set in steps.")

    @origin_dataset.setter
    def origin_dataset(self, data_source: DataWrapper) -> None:
        """Deprecated. Use steps' [`origin_dataset`][vectice.models.Step.origin_dataset] instead.

        Parameters:
            data_source: The origin dataset.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Origin datasets are now set in steps.")

    def phase(self, phase: str | int) -> Phase:
        """Get a phase.

        Parameters:
            phase: The name or id of the phase to get.

        Returns:
            The specified phase.
        """
        item = self._client.get_phase(phase, project_id=self._id)
        _logger.info(f"Phase with id: {item.id} successfully retrieved.")
        phase_object = Phase(item.id, self, item.name, item.index, item.status)
        self._phase = phase_object
        return phase_object

    @property
    def phases(self) -> list[Phase]:
        """The project's phases.

        Returns:
            The phases associated with this project.
        """
        outputs = self._client.list_phases(project=self._id)
        return sorted(
            [Phase(item.id, self, item.name, item.index, item.status) for item in outputs], key=lambda x: x.index
        )
