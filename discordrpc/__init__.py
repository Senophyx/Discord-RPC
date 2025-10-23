from importlib.metadata import version as _pkg_ver
from .presence import RPC
from .button import Button
from .exceptions import *
from .types import *
from .utils import *

__title__ = "Discord RPC"
__version__ = _pkg_ver('discord-rpc')
__authors__ = "Senophyx"
__license__ = "MIT License"
__copyright__ = "Copyright 2021-2025 Senophyx"
