from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING

from vectice.api.json.iteration import IterationStatus

if TYPE_CHECKING:
    from vectice.models.iteration import Iteration


@contextmanager
def hide_logs(package: str):
    old_level = logging.getLogger(package).level
    try:
        logging.getLogger(package).setLevel(logging.ERROR)
        yield
    finally:
        logging.getLogger(package).setLevel(old_level)


def _check_read_only(iteration: Iteration):
    """Check if an iteration is completed or canceled.

    Refreshing the iteration is necessary because in a Jupyter notebook
    its status could have changed on the backend.

    Parameters:
        iteration: The iteration to check.

    Raises:
        RuntimeError: When the iteration is read-only (completed or canceled).
    """
    refresh_iteration = iteration._phase.iteration(iteration.index)
    if refresh_iteration._status in {IterationStatus.Completed, IterationStatus.Abandoned}:
        raise RuntimeError(f"The Iteration is {refresh_iteration._status.name} and is read-only!")
