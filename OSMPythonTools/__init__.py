import logging
import sys

from OSMPythonTools.__info__ import pkgName, pkgVersion, pkgUrl

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def _raiseException(prefix, msg):
    sys.tracebacklimit = None
    msgComplete = '[OSMPythonTools.' + prefix + '] ' + msg
    logger.exception(msgComplete)
    raise(Exception(msgComplete))
