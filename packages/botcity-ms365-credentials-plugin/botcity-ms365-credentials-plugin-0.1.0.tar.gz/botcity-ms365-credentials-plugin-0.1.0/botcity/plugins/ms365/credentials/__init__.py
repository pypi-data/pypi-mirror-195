from . import _version
from .plugin import MS365CredentialsPlugin, Scopes  # noqa: F401, F403

__version__ = _version.get_versions()['version']
