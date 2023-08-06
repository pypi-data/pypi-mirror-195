from __future__ import annotations

import logging
import os
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

import dotenv

from vectice.api import Client
from vectice.models.workspace import Workspace
from vectice.utils.common_utils import hide_logs
from vectice.utils.configuration import Configuration
from vectice.utils.last_assets import _get_last_used_assets_and_logging

if TYPE_CHECKING:
    from vectice.models.project import Project


_logger = logging.getLogger(__name__)
DEFAULT_API_ENDPOINT = "https://app.vectice.com"
CAN_NOT_BE_EMPTY_ERROR_MESSAGE = "%s can not be empty."


class Connection:
    """Connect to the Vectice backend (application).

    The Connection class encapsulates a connection to the Vectice App.
    Thus, it authenticates and connects to Vectice.
    This allows you to start interacting with your Vectice assets.

    A Connection can be initialized in three ways:

    1. Passing the relevant arguments to authenticate and connect to Vectice:

        ```python
        import vectice

        connection = vectice.connect(
            api_token="API_TOKEN_FROM_VECTICE",
            host="https://app.vectice.com",
        )
        ```

    2. Passing the path to a configuration file:

        ```python
        import vectice

        connection = vectice.connect(config="vectice_config.json")
        ```

    3. Letting Vectice find the configuration file in specific locations:

        ```python
        import vectice

        connection = vectice.connect()
        ```

    See [`Connection.connect`][vectice.connection.Connection.connect] for more info.
    """

    USER_FILES_PATH = [
        ".vectice",
        str(Path.home() / ".vectice"),
        ".env",
        str(Path.home() / ".env"),
        "/etc/vectice/api.cfg",
    ]

    def __init__(
        self,
        api_token: str,
        host: str,
        workspace: str | int | None = None,
    ):
        """Initialize a connection.

        Parameters:
            api_token: Your private api token.
            host: The address of the Vectice application.
            workspace: The workspace you want to work in.

        Raises:
            RuntimeError: When the API and backend versions are incompatible.
        """
        logging.getLogger("Client").propagate = True
        self._client = Client(
            workspace=workspace,
            token=api_token,
            api_endpoint=host,
            auto_connect=True,
            allow_self_certificate=True,
        )
        _logger.info("Vectice successfully connected.")
        compatibility = self._client.check_compatibility()
        if compatibility.status != "OK":
            if compatibility.status == "Error":
                _logger.error(f"compatibility error: {compatibility.message}")
                raise RuntimeError(f"compatibility error: {compatibility.message}")
            else:
                _logger.warning(f"compatibility warning: {compatibility.message}")

    def __repr__(self) -> str:
        return (
            "Connection("
            + f"workspace={self._client.workspace.name if self._client.workspace else 'None'}, "
            + f"host={self._client.auth.api_base_url}, "
        )

    @property
    def version_api(self) -> str:
        return self._client.version_api

    @property
    def version_backend(self) -> str:
        return self._client.version_backend

    def workspace(self, workspace: str | int) -> Workspace:
        """Get a workspace.

        Parameters:
            workspace: The id or the name of the desired workspace.

        Returns:
            The desired workspace.
        """
        output = self._client.get_workspace(workspace)
        result = Workspace(output.id, output.name, output.description)
        result.__post_init__(self._client, self)
        return result

    @property
    def workspaces(self) -> list[Workspace] | None:
        """List the workspaces to which this connection has access.

        Returns:
            The workspaces to which this connection has access.
        """
        outputs = self._client.list_workspaces()
        results = [Workspace(id=output.id, name=output.name, description=output.description) for output in outputs.list]
        for workspace in results:
            workspace.__post_init__(self._client, self)
        return results

    @staticmethod
    def connect(
        api_token: str | None = None,
        host: str | None = None,
        config: str | None = None,
        workspace: str | int | None = None,
        project: str | None = None,
    ) -> Connection | Workspace | Project | None:
        """Method to connect to the Vectice backend (application).

        Authentication credentials are retrieved, in order, from:

        1. keyword arguments
        2. configuration file (`config` parameter)
        3. environment variables
        4. environment files in the following order
            - `.vectice` of the working directory
            - `.vectice` of the user home directory
            - `.env` of the working directory
            - `.env` of the user home directory
            - `/etc/vectice/api.cfg` file

        This method uses the `api_token`, `host`, `workspace`, `project` arguments
        or the JSON config provided. The JSON config file is available from the Vectice
        webapp when creating an API token.

        Parameters:
            api_token: The api token provided by the Vectice webapp.
            host: The backend host to which the client will connect.
                If not found, the default endpoint https://app.vectice.com is used.
            config: A JSON config file containing keys VECTICE_API_TOKEN and
                VECTICE_API_ENDPOINT as well as optionally WORKSPACE and PROJECT.
            workspace: The name of an optional workspace to return.
            project: The name of an optional project to return.

        Raises:
            ValueError: When a project is specified without a workspace.

        Returns:
            A Connection, Workspace, or Project.
        """
        host = Connection.get_correct_host(host, config)
        api_token = Connection.get_correct_api_token(api_token, host, config)
        workspace = Connection.get_correct_workspace(workspace, config)
        project = Connection.get_correct_project(project, config)
        connection = Connection(api_token=api_token, host=host)
        if workspace and not project:
            return connection.get_workspace(workspace)
        if workspace and project:
            return connection.get_project(workspace, project)
        if project and not workspace:
            raise ValueError("A workspace reference is needed to retrieve a project.")
        return connection

    @classmethod
    def get_correct_host(cls, host: str | None, config: str | None) -> str:
        host = Connection.get_information_from_next_layers(host, "VECTICE_API_ENDPOINT", config)  # type: ignore[assignment]
        if not host:
            _logger.info(f"No VECTICE_API_ENDPOINT provided. Using default endpoint {DEFAULT_API_ENDPOINT}")
            return DEFAULT_API_ENDPOINT
        return host

    @classmethod
    def get_correct_api_token(cls, api_token: str | None, host: str | None, config: str | None) -> str:
        token = Connection.get_information_from_next_layers(api_token, "VECTICE_API_TOKEN", config)
        if token is None:
            raise ValueError(
                f"You must provide the api_token. You can generate them by going to the page {host}/account/api-keys"
            )
        return token  # type: ignore[return-value]

    @classmethod
    def get_correct_workspace(cls, workspace, config) -> str | int | None:
        return Connection.get_information_from_next_layers(workspace, "WORKSPACE", config)

    @classmethod
    def get_correct_project(cls, project, config) -> str | None:
        return Connection.get_information_from_next_layers(project, "PROJECT", config)  # type: ignore[return-value]

    @classmethod
    def get_information_from_next_layers(
        cls, information: str | None, information_key: str, config: str | None
    ) -> str | int | None:
        if information:
            return information
        if config:
            with suppress(KeyError):
                return Configuration(config)[information_key]
        information = os.environ.get(information_key, "")
        if information:
            _logger.info(f"Found {information_key} in environment variables.")
            return information
        return Connection.get_information_from_user_files(information_key)

    @classmethod
    def get_information_from_user_files(cls, information_key: str) -> str | None:
        for path in cls.USER_FILES_PATH:
            with hide_logs("dotenv"):
                information = dotenv.get_key(path, information_key)
                if information:
                    _logger.info(f"Found {information_key} in {path}")
                    return information
        return None

    def get_workspace(self, workspace: int | str) -> Workspace:
        workspace_output: Workspace = self.workspace(workspace)
        _logger.info(f"Your current workspace: {workspace_output.name}")
        _get_last_used_assets_and_logging(self._client, _logger, workspace_output.name)
        return workspace_output

    def get_project(self, workspace: int | str, project: str) -> Project:
        logging.getLogger("vectice.models.workspace").propagate = False
        workspace_output = self.workspace(workspace)
        project_output: Project = workspace_output.project(project)
        _logger.info(f"Your current workspace: {workspace_output.name} and project: {project_output.name}")
        _get_last_used_assets_and_logging(self._client, _logger, workspace_output.name)
        return project_output
