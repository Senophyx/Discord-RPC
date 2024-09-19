import logging

from .exceptions import *
from .presence import RPC
from .button import Button
from .utils import get_timestamp, timestamp, date_to_timestamp

__title__ = "Discord RPC"
__version__ = "5.1b1"
__authors__ = "Senophyx"
__license__ = "MIT License"
__copyright__ = "Copyright 2021-2024 Senophyx"

logging.getLogger(__name__).addHandler(logging.NullHandler())
