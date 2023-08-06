"""Schema."""
from .. import __version__ as _version

_schema_id = "cbwk"
_name = "hub"
_migration = "1fdc05837919"
__version__ = _version

from . import versions  # noqa
from ._core import Account, Instance, Organization, Storage, User  # noqa
