from typing_extensions import TypeAlias
from importlib_metadata import version

__version__ = version("chatnoir-pyterrier")

from logging import getLogger

from chatnoir_pyterrier import retrieve, feature
import chatnoir_api as api

logger = getLogger("chatnoir-pyterrier")

# Re-export from child modules.
Feature = feature.Feature
ChatNoirRetrieve = retrieve.ChatNoirRetrieve

# Re-export from `chatnoir-api`.
Index: TypeAlias = api.Index
