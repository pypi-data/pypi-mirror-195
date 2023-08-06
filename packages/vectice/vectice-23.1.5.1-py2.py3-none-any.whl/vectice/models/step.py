from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.http_error_handlers import VecticeException
from vectice.api.json.iteration import IterationStepArtifactInput
from vectice.models.datasource.datawrapper import DataWrapper
from vectice.models.datasource.datawrapper.metadata import SourceUsage
from vectice.models.git_version import _check_code_source, _inform_if_git_repo
from vectice.utils.automatic_link_utils import existing_dataset_logger, link_assets_to_step, link_dataset_to_step
from vectice.utils.common_utils import _check_read_only

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api.json.iteration import IterationStepArtifact
    from vectice.models import Iteration, Phase, Project, Workspace


_logger = logging.getLogger(__name__)

MISSING_DATASOURCE_ERROR_MESSAGE = "Cannot create modeling dataset. Missing %s data source."


class Step:
    """Model a Vectice step.

    Steps define the logical sequence of steps required to complete
    the phase along with their expected outcomes.

    Steps belong to an Iteration. The steps created under a Phase are
    Step Definitions that are then re-used in Iterations to iteratively
    complete the steps until a satisfactory result is obtained.

    ```tree
    phase 1
        step definition 1
        step definition 2
        step definition 3
    ```

    ```tree
    iteration 1 of phase 1
        step 1
        step 2
        step 3
    ```

    If steps are added to a phase after iterations have been created
    and completed, these steps won't appear in these iterations.

    NOTE: **Phases and Steps Definitions are created in the Vectice App,
    Iterations are created from the Vectice Python API.**

    To complete an iteration's step, you just need to assign a value to it.
    To access the step and assign a value, you can use the "slug" of the step:
    the slug is the name of the step, transformed to fit Python's naming rules,
    and prefixed with `step_`. For example, a step called "Clean Dataset" can
    be accessed with `my_iteration.step_clean_dataset`.

    Therefore, to complete a step:

    ```python
    my_clean_dataset = ...
    my_iteration.step_clean_dataset = my_clean_dataset
    ```

    Depending on the step, you can assign it a [`Model`][vectice.models.model.Model],
    a data source, code source, or attachments.
    """

    def __init__(
        self,
        id: int,
        iteration: Iteration,
        name: str,
        index: int,
        description: str | None = None,
        completed: bool = False,
        artifacts: list[IterationStepArtifact] | None = None,
    ):
        """
        Initialize a step.

        Vectice users shouldn't need to instantiate Steps manually,
        but here are the step parameters.

        Parameters:
            id: The step identifier.
            iteration: The iteration to which the step belongs.
            name: The name of the step.
            index: The index of the step.
            description: The description of the step.
            completed: Whether the step is completed.
            artifacts: The artifacts linked to the steps.
        """
        self._id = id
        self._iteration: Iteration = iteration
        self._name = name
        self._index = index
        self._description = description
        self._client = self._iteration._client
        self._completed = completed
        self._artifacts = artifacts
        self._origin_dataset: DataWrapper | None = None
        self._clean_dataset: DataWrapper | None = None
        self._modeling_dataset: tuple[DataWrapper, DataWrapper, DataWrapper] | None = None

        if completed:
            _logger.warning(f"The Step {name} is completed!")

    def __repr__(self):
        return f"Step(name='{self.name}', id={self.id}, description='{self._description}', completed={self.completed})"

    def __eq__(self, other: object):
        if not isinstance(other, Step):
            return NotImplemented
        return self.id == other.id

    @property
    def name(self) -> str:
        """The step's name.

        Returns:
            The step's name.
        """
        return self._name

    @property
    def id(self) -> int:
        """The step's id.

        Returns:
            The step's id.
        """
        return self._id

    @id.setter
    def id(self, step_id: int):
        """Set the step's id.

        Parameters:
            step_id: The id to set.
        """
        self._id = step_id

    @property
    def index(self) -> int:
        """The step's index.

        Returns:
            The step's index.
        """
        return self._index

    @property
    def properties(self) -> dict:
        """The step's name, id, and index.

        Returns:
            A dictionary containing the `name`, `id` and `index` items.
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def artifacts(self) -> list[IterationStepArtifact] | None:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts: list[IterationStepArtifact]):
        self._artifacts = artifacts

    def next_step(self, message: str | None = None) -> Step | None:
        """Advance to the next step.

        Close the current step (mark it completed) and return the next
        step to complete if another open step exists. Otherwise return None.

        Note that steps are not currently ordered, and so the concept
        of "next" is rather arbitrary.

        Parameters:
            message: The message to use when closing the current step.

        Returns:
            The next step.
        """
        try:
            self.close(message)
        except VecticeException:
            _logger.info("The step is closed!")
            return None
        steps_output = self._client.list_steps(self._iteration._phase.id, self._iteration.index)
        open_steps = sorted(
            [
                Step(item.id, self._iteration, item.name, item.index, item.description)
                for item in steps_output
                if not item.completed
            ],
            key=lambda x: x.index,
        )
        if not open_steps:
            _logger.info("There are no active steps.")
            return None
        next_step = open_steps[0]
        _logger.info(f"Next step : {repr(next_step)}")
        return next_step

    def close(self, message: str | None = None):
        """Close the current step, marking it completed.

        Parameters:
            message: The message to use when closing the step.
        """
        self._client.close_step(self.id, message)
        _logger.info(f"'{self.name}' was successfully closed.")
        self._completed = True

    @property
    def connection(self) -> Connection:
        """The connection to which this step belongs.

        Returns:
            The connection to which this step belongs.
        """
        return self._iteration.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this step belongs.

        Returns:
            The workspace to which this step belongs.
        """
        return self._iteration.workspace

    @property
    def project(self) -> Project:
        """The project to which this step belongs.

        Returns:
            The project to which this step belongs.
        """
        return self._iteration.project

    @property
    def phase(self) -> Phase:
        """The phase to which this step belongs.

        Returns:
            The phase to which this step belongs.
        """
        return self._iteration.phase

    @property
    def iteration(self) -> Iteration:
        """The iteration to which this step belongs.

        Returns:
            The iteration to which this step belongs.
        """
        return self._iteration

    @property
    def origin_dataset(self) -> DataWrapper | None:
        """The wrapped origin dataset of the step.

        Returns:
            The origin dataset, or None if there is none.
        """
        return self._origin_dataset

    @origin_dataset.setter
    def origin_dataset(self, data_source: DataWrapper):
        """Set the wrapped origin dataset of the step.

        Parameters:
            data_source: The origin dataset.
        """
        _check_read_only(self.iteration)

        code_version_id = self._get_code_version_id()
        self._origin_dataset = data_source
        data = self._client.register_dataset_from_source(
            data_source,
            SourceUsage.ORIGIN,
            project_id=self.project.id,
            phase_id=self.phase.id,
            iteration_id=self.iteration.id,
            code_version_id=code_version_id,
        )
        existing_dataset_logger(data, data_source.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        link_dataset_to_step(step_artifact, data_source, data, _logger, self, SourceUsage.ORIGIN)

    @property
    def clean_dataset(self) -> DataWrapper | None:
        """The step's cleaned dataset.

        If the step has no assigned cleaned dataset, return None.

        Returns:
            The step's cleaned dataset, or None.
        """
        return self._clean_dataset

    @clean_dataset.setter
    def clean_dataset(self, data_source: DataWrapper) -> None:
        """Set the step's cleaned dataset.

        Parameters:
            data_source: The cleaned dataset.
        """
        _check_read_only(self.iteration)
        code_version_id = self._get_code_version_id()
        self._clean_dataset = data_source
        data = self._client.register_dataset_from_source(
            data_source,
            SourceUsage.CLEAN,
            project_id=self.project.id,
            phase_id=self.phase.id,
            iteration_id=self.iteration.id,
            code_version_id=code_version_id,
        )
        existing_dataset_logger(data, data_source.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        logging.getLogger("vectice.models.project").propagate = False
        link_dataset_to_step(step_artifact, data_source, data, _logger, self, SourceUsage.CLEAN)

    @property
    def modeling_dataset(
        self,
    ) -> tuple[DataWrapper, DataWrapper, DataWrapper] | None:
        """The iteration's modeling dataset.

        Returns:
            The training set.
            The test set.
            The validation set.
        """
        return self._modeling_dataset

    @modeling_dataset.setter
    def modeling_dataset(self, data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]):
        """Set a modeling dataset.

        Provides training, testing and validation datasources, the
        order of which does not matter (despite it being a tuple) and
        the combination of the data sources does not either. Thus, you
        could use whatever combination suites your needs.

        The DataWraper can be accessed via vectice.FileDataWrapper,
        vectice.GcsDataWrapper and vectice.S3DataWrapper.

        Or for example `from vectice import FileDataWrapper`.

        Parameters:
            data_sources: A tuple of three datasources; their metadata
                must be of three types: training, testing and validation.
        """
        # TODO: refactor to break cyclic import
        from vectice.api.json.dataset_register import DatasetRegisterInput

        _check_read_only(self.iteration)
        logging.getLogger("vectice.models.iteration").propagate = True
        code_version_id = self._get_code_version_id()
        train_datasource, test_datasource, validation_datasource = self._get_datasources_in_order(data_sources)
        self._modeling_dataset = train_datasource, test_datasource, validation_datasource

        name = self._client.get_dataset_name(train_datasource)
        derived_from = self._client.get_dataset_derived_from(train_datasource)
        dataset_sources = self._get_metadata_from_sources((train_datasource, test_datasource, validation_datasource))
        dataset_register_input = DatasetRegisterInput(
            name=name,
            type=SourceUsage.MODELING.value,
            datasetSources=dataset_sources,
            inputs=derived_from,
            codeVersionId=code_version_id,
        )
        data = self._client.register_dataset(
            dataset_register_input,
            iteration_id=self.iteration.id,
            project_id=self.project.id,
            phase_id=self.phase.id,
        )
        existing_dataset_logger(data, name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self.iteration, step_artifact, name, data, _logger)

    @staticmethod
    def _get_datasources_in_order(
        data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]
    ) -> tuple[DataWrapper, DataWrapper, DataWrapper]:
        from vectice import DatasetSourceUsage

        if len(data_sources) != 3:
            raise ValueError("Exactly three datasources are needed to create a modeling dataset.")
        train_datasource, test_datasource, validation_datasource = None, None, None
        for data_source in data_sources:
            if data_source.metadata.usage == DatasetSourceUsage.TRAINING:
                train_datasource = data_source
            elif data_source.metadata.usage == DatasetSourceUsage.TESTING:
                test_datasource = data_source
            elif data_source.metadata.usage == DatasetSourceUsage.VALIDATION:
                validation_datasource = data_source
        if not train_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "training")
        if not test_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "testing")
        if not validation_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "validation")
        return train_datasource, test_datasource, validation_datasource

    @staticmethod
    def _get_metadata_from_sources(data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]) -> list[dict]:
        return [data_source.metadata.asdict() for data_source in data_sources if data_source]

    def _get_code_version_id(self):
        from vectice import code_capture

        if code_capture:
            return _check_code_source(self._client, self.project.id, _logger)
        else:
            _inform_if_git_repo(_logger)
            return None
