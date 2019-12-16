"""Metadata generation logic for source distributions.
"""

import logging
import os

from pip._internal.utils.subprocess import runner_with_spinner_message
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from pip._internal.build_env import BuildEnvironment
    from pip._vendor.pep517.wrappers import Pep517HookCaller

logger = logging.getLogger(__name__)


def generate_metadata(build_env, backend):
    # type: (BuildEnvironment, Pep517HookCaller) -> str
    """Generate metadata using mechanisms described in PEP 517.

    Returns the generated metadata directory.
    """
    assert backend is not None

    metadata_tmpdir = TempDirectory(
        kind="modern-metadata", globally_managed=True
    )

    metadata_dir = metadata_tmpdir.path

    with build_env:
        # Note that Pep517HookCaller implements a fallback for
        # prepare_metadata_for_build_wheel, so we don't have to
        # consider the possibility that this hook doesn't exist.
        runner = runner_with_spinner_message("Preparing wheel metadata")
        with backend.subprocess_runner(runner):
            distinfo_dir = backend.prepare_metadata_for_build_wheel(
                metadata_dir
            )

    return os.path.join(metadata_dir, distinfo_dir)
