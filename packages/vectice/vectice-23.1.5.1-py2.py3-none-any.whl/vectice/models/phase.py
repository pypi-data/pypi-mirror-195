from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.json.phase import PhaseStatus
from vectice.models.datasource.datawrapper import DataWrapper
from vectice.models.iteration import Iteration
from vectice.utils.deprecation import DeprecationError

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client
    from vectice.models import Project, Workspace


_logger = logging.getLogger(__name__)


class Phase:
    """Represent a Vectice phase.

    Phases reflect the real-life phases of the project lifecycle
    (i.e., Business Understanding, Data Preparation, Modeling,
    Deployment, etc.).  The Vectice admin creates the phases of a
    project.

    Phases let you document the goals, assets, and outcomes along with
    the status to organize the project, enforce best practices, allow
    consistency, and capture knowledge.

    Phases contain definitions of steps that are performed
    by data-scientists in order to complete iterations.

    ```tree
    phase 1
        step definition 1
        step definition 2
        step definition 3
    ```

    To get a project's phase:

    ```python
    my_phase = my_project.phase("Business Understanding")
    ```

    Iterations can then be created for this phase,
    to complete the phase steps:

    ```python
    my_origin_dataset = ...
    my_iteration = my_phase.iteration()
    my_iteration.step_origin_dataset = my_origin_dataset
    ```

    NOTE: **Phases and Steps Definitions are created in the Vectice App,
    Iterations are created from the Vectice Python API.**

    See the documentation of [Iterations][vectice.models.Iteration]
    for more information about iterations.
    """

    __slots__ = [
        "_id",
        "_project",
        "_name",
        "_index",
        "_status",
        "_client",
        "_current_iteration",
        "_pointers",
    ]

    def __init__(
        self,
        id: int,
        project: Project,
        name: str,
        index: int,
        status: PhaseStatus = PhaseStatus.NotStarted,
    ):
        """Initialize a phase.

        Vectice users shouldn't need to instantiate Phases manually,
        but here are the phase parameters.

        Parameters:
            id: The phase identifier.
            project: The project to which the phase belongs.
            name: The name of the phase.
            index: The index of the phase.
            status: The status of the phase.
        """
        self._id = id
        self._project = project
        self._name = name
        self._index = index
        self._status = status
        self._client: Client = self._project._client
        self._current_iteration: Iteration | None = None

    def __repr__(self):
        return f"Phase (name='{self.name}', id={self.id}, status='{self.status.name}')"

    def __eq__(self, other: object):
        if not isinstance(other, Phase):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """The phase's id.

        Returns:
            The phase's id.
        """
        return self._id

    @id.setter
    def id(self, phase_id: int):
        """Set the phase's id.

        Parameters:
            phase_id: The phase id to set.
        """
        self._id = phase_id

    @property
    def name(self) -> str:
        """The phase's name.

        Returns:
            The phase's name.
        """
        return self._name

    @property
    def index(self) -> int:
        """The phase's index.

        Returns:
            The phase's index.
        """
        return self._index

    @property
    def status(self) -> PhaseStatus:
        """The phase's status.

        Returns:
            The phase's status.
        """
        return self._status

    @property
    def properties(self) -> dict:
        """The phase's name, id, and index.

        Returns:
            A dictionary containing the `name`, `id`, and `index` items.
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def iterations(self) -> list[Iteration]:
        """The phase's iterations.

        Returns:
            The phase's iterations.
        """
        iteration_outputs = self._client.list_iterations(self.id)
        return sorted(
            [Iteration(item.id, item.index, self, item.status) for item in iteration_outputs], key=lambda x: x.index
        )

    @property
    def clean_dataset(self) -> None:
        """Deprecated. Use steps' [`clean_dataset`][vectice.models.Step.clean_dataset] instead.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Clean datasets are now set in steps.")

    @clean_dataset.setter
    def clean_dataset(self, data_source: DataWrapper) -> None:
        """Deprecated. Use steps' [`clean_dataset`][vectice.models.Step.clean_dataset] instead.

        Parameters:
            data_source: The cleaned dataset.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Clean datasets are now set in steps.")

    def iteration(self, index: int | None = None) -> Iteration:
        """Get a (possibly new) iteration.

        Fetch and return an iteration by index. If no index is
        provided, return a new iteration.

        Parameters:
            index: The id of an existing iteration.

        Returns:
            An iteration.
        """
        if index:
            iteration_output = self._client.get_iteration_by_index(self.id, index)
        else:
            iteration_output = self._client.get_or_create_iteration(self.id)
        _logger.info(f"Iteration number {iteration_output.index} (id {iteration_output.id}) successfully retrieved.")
        iteration_object = Iteration(iteration_output.id, iteration_output.index, self, iteration_output.status)
        self._current_iteration = iteration_object
        return iteration_object

    @property
    def connection(self) -> Connection:
        """The connection to which this phase belongs.

        Returns:
            The connection to which this phase belongs.
        """
        return self._project.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this phase belongs.

        Returns:
            The workspace to which this phase belongs.
        """
        return self._project.workspace

    @property
    def project(self) -> Project:
        """The project to which this phase belongs.

        Returns:
            The project to which this phase belongs.
        """
        return self._project
