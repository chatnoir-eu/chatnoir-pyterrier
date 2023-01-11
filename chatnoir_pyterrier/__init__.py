from importlib_metadata import version

__version__ = version("chatnoir-api")

from logging import getLogger

from chatnoir_pyterrier import retrieve, feature

logger = getLogger("chatnoir-pyterrier")

# Re-export from child modules.
Feature = feature.Feature
ChatNoirRetrieve = retrieve.ChatNoirRetrieve
