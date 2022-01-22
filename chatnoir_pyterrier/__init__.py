__version__ = "0.1.0"

from logging import getLogger

from chatnoir_pyterrier.retrieve import (
    Feature as ExportFeature, ChatNoirRetrieve as ExportChatNoirRetrieve
)

logger = getLogger("chatnoir-pyterrier")

# Re-export from child modules.
Feature = ExportFeature
ChatNoirRetrieve = ExportChatNoirRetrieve
