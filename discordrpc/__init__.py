from importlib.metadata import version as _pkg_ver, PackageNotFoundError
from .presence import RPC
from .button import Button
from .exceptions import *
from .types import *
from .utils import *

__title__ = "Discord RPC"
try:
    __version__ = _pkg_ver('discord-rpc')
except PackageNotFoundError:
    __version__ = "unknown"
__authors__ = "Senophyx"
__license__ = "MIT License"
__copyright__ = "Copyright 2021-2025 Senophyx"
