from __future__ import annotations

from enum import Enum


class DatasetSourceUsage(Enum):
    """Enumeration that defines the usage of the dataset."""

    TRAINING = "TRAINING"
    """For training datasets."""
    TESTING = "TESTING"
    """For testing datasets."""
    VALIDATION = "VALIDATION"
    """For validation datasets."""


class SourceOrigin(Enum):
    """Enumeration that defines where the data comes from."""

    S3 = "S3"
    """S3 storage."""
    REDSHIFT = "REDSHIFT"
    """Redshift storage."""
    GCS = "GCS"
    """Google Cloud Storage."""
    BIGQUERY = "BIGQUERY"
    """BigQuery storage."""
    SNOWFLAKE = "SNOWFLAKE"
    """Snowflake storage."""
    OTHER = "OTHER"
    """Other storage."""


class Metadata:
    """This class describes the metadata of a file."""

    def __init__(
        self,
        size: int,
        type: str,
        origin: str,
        usage: DatasetSourceUsage | None = None,
    ):
        """Initialize a metadata instance.

        Parameters:
            size: The size of the file.
            origin: The origin of the file.
            type: The type of data, database or files.
            usage: The usage of the file.
        """
        self.origin = origin
        self.size = size
        self.usage = usage
        self.type = type


class SourceType(Enum):
    """Enumeration that defines the type of the source the data comes from."""

    DB = "DB"
    """DB source."""
    FILES = "FILES"
    """Files source."""


class SourceUsage(Enum):
    """Enumeration that defines the usage of the data source."""

    ORIGIN = "ORIGIN"
    """Used as origin source."""
    CLEAN = "CLEAN"
    """Used as clean source."""
    VALIDATION = "VALIDATION"
    """Used as validation source."""
    MODELING = "MODELING"
    """Used as modeling source."""
