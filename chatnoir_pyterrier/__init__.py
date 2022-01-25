__version__ = "1.0.2"

from logging import getLogger

from chatnoir_pyterrier import retrieve, feature

logger = getLogger("chatnoir-pyterrier")

# Re-export from child modules.
Feature = feature.Feature
ChatNoirRetrieve = retrieve.ChatNoirRetrieve
