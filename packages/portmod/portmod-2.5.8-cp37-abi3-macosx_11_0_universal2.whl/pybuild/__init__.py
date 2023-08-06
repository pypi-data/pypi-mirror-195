# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
The module accessible within pybuilds

Note that this module should not be imported outside of pybuild files
"""

from portmodlib._deprecated import (  # noqa  # pylint: disable=unused-import
    File,
    InstallDir,
)
from portmodlib._deprecated.vfs import (  # noqa  # pylint: disable=unused-import
    find_file,
    list_dir,
)
from portmodlib.atom import version_gt  # noqa  # pylint: disable=unused-import
from portmodlib.fs import patch_dir  # noqa  # pylint: disable=unused-import
from portmodlib.globals import download_dir as _download_dir
from portmodlib.masters import get_masters  # noqa  # pylint: disable=unused-import
from portmodlib.usestr import (  # noqa  # pylint: disable=unused-import
    check_required_use,
    use_reduce,
)

from ._pybuild import (  # noqa  # pylint: disable=unused-import
    Pybuild1,
    Pybuild2,
    apply_patch,
)

DOWNLOAD_DIR = _download_dir()

__all__ = [
    "version_gt",
    "patch_dir",
    "get_masters",
    "use_reduce",
    "find_file",
    "list_dir",
    "File",
    "InstallDir",
    "Pybuild1",
    "Pybuild2",
    "apply_patch",
    "DOWNLOAD_DIR",
]
