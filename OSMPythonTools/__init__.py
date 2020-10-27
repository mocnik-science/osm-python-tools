import logging

from OSMPythonTools.__info__ import pkgName, pkgVersion, pkgUrl

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def _raiseException(prefix, msg):
    sys.tracebacklimit = None
    msgComplete = '[OSMPythonTools.' + prefix + '] ' + msg
    OSMPythonTools.logger.exception(msgComplete)
    raise(Exception(msgComplete))
