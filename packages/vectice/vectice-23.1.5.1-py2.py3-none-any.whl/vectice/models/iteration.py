from __future__ import annotations

import logging
import pickle  # nosec
from contextlib import suppress
from typing import TYPE_CHECKING, Any

from vectice.api.http_error_handlers import NoStepsInPhaseError
from vectice.api.json.iteration import IterationInput, IterationStatus, IterationStepArtifactInput
from vectice.api.json.model_version import ModelVersionOutput
from vectice.models.attachment_container import AttachmentContainer
from vectice.models.git_version import _check_code_source, _inform_if_git_repo
from vectice.utils.automatic_link_utils import existing_model_logger, link_assets_to_step
from vectice.utils.common_utils import _check_read_only
from vectice.utils.deprecation import DeprecationError

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client
    from vectice.models import Phase, Project, Step, Workspace
    from vectice.models.datasource.datawrapper import DataWrapper
    from vectice.models.model import Model

_logger = logging.getLogger(__name__)


class Iteration:
    """Represent a Vectice iteration.

    Iterations reflect the model development and test cycles completed
    by data scientists until a fully functional algorithm is ready for
    deployment.  Each iteration contains the sequence of steps defined
    at the Phase and acts as a guardrail for data scientists to
    provide their updates.

    If steps are added to a phase after iterations have been created
    and completed, these steps won't appear in these iterations.

    ```tree
    iteration 1
        step 1
        step 2
        step 3
    ```

    NOTE: **Phases and Steps Definitions are created in the Vectice App,
    Iterations are created from the Vectice Python API.**

    To create a new iteration:

    ```python
    my_iteration = my_phase.iteration()
    ```
    """

    __slots__ = [
        "_id",
        "_index",
        "_phase",
        "_status",
        "_client",
        "_model",
        "_current_step",
        "_pointers",
        "_step",
        "_steps",
    ]

    def __init__(
        self,
        id: int,
        index: int,
        phase: Phase,
        status: IterationStatus | None = IterationStatus.NotStarted,
    ):
        """Initialize an iteration.

        Vectice users shouldn't need to instantiate Iterations manually,
        but here are the iteration parameters.

        Parameters:
            id: The iteration identifier.
            index: The index of the iteration.
            phase: The project to which the iteration belongs.
            status: The status of the iteration.
        """
        self._id = id
        self._index = index
        self._phase = phase
        self._status = status
        self._client: Client = self._phase._client
        self._model: Model | None = None
        self._current_step: Step | None = None
        self._steps = self._populate_steps()

    def __repr__(self):
        steps = len(self.steps)
        return f"Iteration (index={self._index}, status={self._status}, No. of steps={steps})"

    def __eq__(self, other: object):
        if not isinstance(other, Iteration):
            return NotImplemented
        return self.id == other.id

    def _populate_steps(self):
        with suppress(NoStepsInPhaseError):
            return {name: None for name in self.step_names}
        return {}

    @property
    def id(self) -> int:
        """The iteration's identifier.

        Returns:
            The iteration's identifier.
        """
        return self._id

    @id.setter
    def id(self, iteration_id: int):
        """Set the iteration's identifier.

        Parameters:
            iteration_id: The identifier.
        """
        _check_read_only(self)
        self._id = iteration_id

    @property
    def index(self) -> int:
        """The iteration's index.

        Returns:
            The iteration's index.
        """
        return self._index

    @property
    def properties(self) -> dict:
        """The iteration's identifier and index.

        Returns:
            A dictionary containing the `id` and `index` items.
        """
        return {"id": self.id, "index": self.index}

    @property
    def step_names(self) -> list[str]:
        """The names of the steps required in this iteration.

        Returns:
            The steps names.
        """
        return [step.name for step in self.steps]

    def step(self, step: str) -> Step:
        """Get a step by name.

        Step names are configured for a phase by the Vectice administrator.

        Parameters:
            step: The name of the step

        Returns:
            A step.
        """
        from vectice.models import Step

        steps_output = self._client.get_step_by_name(step, self.id)
        _logger.info(f"Step: {steps_output.name} successfully retrieved.")
        step_object = Step(
            steps_output.id,
            self,
            steps_output.name,
            steps_output.index,
            steps_output.description,
            steps_output.completed,
            steps_output.artifacts,
        )
        self._current_step = step_object
        return step_object

    @property
    def steps(self) -> list[Step]:
        """The steps required in this iteration.

        Returns:
            The steps required in this iteration.
        """
        from vectice.models import Step

        steps_output = self._client.list_steps(self._phase.id, self.index, self._phase.name)
        return sorted(
            [Step(item.id, self, item.name, item.index, item.description, item.completed) for item in steps_output],
            key=lambda x: x.index,
        )

    @property
    def model(self) -> Model | None:
        """The iteration's model.

        Returns:
            The iteration's model.
        """
        return self._model

    @model.setter
    def model(self, model: Model):
        """Set the model for the iteration.

        The model can be created using the Model Wrapper, accessed via
        vectice.Model or `from vectice import Model`.

        Parameters:
            model: The model.
        """
        from vectice import code_capture

        _check_read_only(self)
        logging.getLogger("vectice.models.iteration").propagate = True
        if code_capture:
            code_version_id = _check_code_source(self._client, self._phase._project._id, _logger)
        else:
            _inform_if_git_repo(_logger)
            code_version_id = None
        self._model = model
        model_output = self._client.register_model(
            model, self._phase._project._id, self._phase.id, self._id, code_version_id, model.derived_from
        )
        model_version = model_output.model_version
        attachments = self._set_model_attachments(model, model_version)
        _logger.info(
            f"Successfully registered Model(name='{model.name}', library='{model.library}', "
            f"technique='{model.technique}', version='{model_version.name}')."
        )
        existing_model_logger(model_output, model.name, _logger)
        step_artifact = IterationStepArtifactInput(id=model_output["modelVersion"]["id"], type="ModelVersion")
        attachments = (
            [
                IterationStepArtifactInput(id=attach["fileId"], entityFileId=attach["entityId"], type="EntityFile")
                for attach in attachments
            ]
            if attachments
            else None
        )
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self, step_artifact, model.name, model_output, _logger, attachments)

    def cancel(self) -> None:
        """Cancel the iteration by abandoning all unfinished steps."""
        iteration_input = IterationInput(status=IterationStatus.Abandoned.name)
        self._client.update_iteration(self.id, iteration_input)
        self._status = IterationStatus.Abandoned

    def _set_model_attachments(self, model: Model, model_version: ModelVersionOutput):
        logging.getLogger("vectice.models.attachment_container").propagate = True
        attachments = None
        if model.attachments:
            container = AttachmentContainer(model_version, self._client)
            attachments = container.add_attachments(model.attachments)
        if model.predictor:
            model_content = self._serialize_model(model.predictor)
            model_type_name = type(model.predictor).__name__
            container = AttachmentContainer(model_version, self._client)
            container.add_serialized_model(model_type_name, model_content)
        return attachments

    @staticmethod
    def _serialize_model(model: Any) -> bytes:
        return pickle.dumps(model)

    @property
    def connection(self) -> Connection:
        """The connection to which this iteration belongs.

        Returns:
            The connection to which this iteration belongs.
        """
        return self._phase.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this iteration belongs.

        Returns:
            The workspace to which this iteration belongs.
        """
        return self._phase.workspace

    @property
    def project(self) -> Project:
        """The project to which this iteration belongs.

        Returns:
            The project to which this iteration belongs.
        """
        return self._phase.project

    @property
    def phase(self) -> Phase:
        """The phase to which this iteration belongs.

        Returns:
            The phase to which this iteration belongs.
        """
        return self._phase

    @property
    def modeling_dataset(self) -> None:
        """Deprecated. Use steps' [`modeling_dataset`][vectice.models.Step.modeling_dataset] instead.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Modeling datasets are now set in steps.")

    @modeling_dataset.setter
    def modeling_dataset(self, data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]) -> None:
        """Deprecated. Use steps' [`modeling_dataset`][vectice.models.Step.modeling_dataset] instead.

        Parameters:
            data_sources: A tuple of three datasources; their metadata
                must be of three types: training, testing and validation.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Modeling datasets are now set in steps.")
