from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from vectice.utils.deprecation import deprecate

if TYPE_CHECKING:
    from vectice.models.datasource.datawrapper.metadata import DatasetSourceUsage, FilesMetadata

_logger = logging.getLogger(__name__)


class DataWrapper(metaclass=ABCMeta):
    """Base class for DataWrapper.

    Use DataWrapper subclasses to assign datasets to steps.  The
    Vectice library supports a handful of common cases.  Additional
    cases are generally easy to supply by deriving from this base
    class.  In particular, subclasses must override this class'
    abstact methods (`_build_metadata()`, `_fetch_data()`).

    """

    @abstractmethod
    @deprecate(
        parameter="inputs",
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'inputs' parameter is renamed 'derived_from'. "
        "Using 'inputs' will raise an error in v{fail_at}. "
        "The parameter will be removed in v{remove_at}.",
    )
    def __init__(
        self,
        name: str,
        usage: DatasetSourceUsage | None = None,
        derived_from: list[int] | None = None,
        inputs: list[int] | None = None,
    ):
        """Initialize a data wrapper.

        Parameters:
            usage: The usage of the dataset.
            name: The name of the [`DataWrapper`][vectice.models.datasource.datawrapper.data_wrapper.DataWrapper].
            derived_from: The list of dataset ids to create a new dataset from.
            inputs: Deprecated. Use `derived_from` instead.
        """
        if not derived_from and inputs:
            derived_from = inputs

        self._old_name = name
        self._name = name
        self._derived_from = derived_from
        self._usage = usage
        self._metadata = None
        self._data = None

    @property
    def data(self) -> dict[str, bytes]:
        """The wrapper's data.

        Returns:
            The wrapper's data.
        """
        if self._data is None:
            self._data = self._fetch_data()  # type: ignore[assignment]
        return self._data  # type: ignore[return-value]

    @abstractmethod
    def _fetch_data(self) -> dict[str, bytes]:
        pass

    @abstractmethod
    def _build_metadata(self) -> FilesMetadata:
        pass

    @property
    def name(self) -> str:
        """The wrapper's name.

        Returns:
            The wrapper's name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set the wrapper's name.

        Parameters:
            value: The wrapper's name.
        """
        self._name = value
        self._clear_data_and_metadata()

    @property
    def usage(self) -> DatasetSourceUsage | None:
        """The wrapper's usage.

        Returns:
            The wrapper's usage.
        """
        return self._usage

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'inputs' property is renamed 'derived_from'. "
        "Using 'inputs' will raise an error in v{fail_at}. "
        "The property will be removed in v{remove_at}.",
    )
    def inputs(self) -> list[int] | None:
        """Deprecated. Use `derived_from` instead.

        Returns:
            The datasets from which this wrapper is derived.
        """
        return self.derived_from

    @property
    def derived_from(self) -> list[int] | None:
        """The datasets from which this wrapper is derived.

        Returns:
            The datasets from which this wrapper is derived.
        """
        return self._derived_from

    @property
    def metadata(self) -> FilesMetadata:
        """The wrapper's metadata.

        Returns:
            The wrapper's metadata.
        """
        if self._metadata is None:
            self.metadata = self._build_metadata()
        return self._metadata  # type: ignore[return-value]

    @metadata.setter
    def metadata(self, value):
        """Set the wrapper's metadata.

        Parameters:
            value: The metadata to set.
        """
        self._metadata = value

    def _clear_data_and_metadata(self):
        self._data = None
        self._metadata = None
