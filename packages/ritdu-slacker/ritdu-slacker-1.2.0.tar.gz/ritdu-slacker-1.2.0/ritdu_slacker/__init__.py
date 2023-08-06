import logging

from signal import signal, SIGINT
from sys import exit

from pbr.version import VersionInfo
from ritdu_slacker.constants import TOOL_NAME



TOOL_NAME = 'ritdu-slacker'
TOOL_VERSION = VersionInfo(TOOL_NAME).release_string()

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logging.basicConfig(
    format=f'[%(asctime)s] {TOOL_NAME} [%(levelname)s] %(funcName)s %(lineno)d: %(message)s'
)


def sigint_handler(signal_received, frame):
    """Handle SIGINT or CTRL-C and exit gracefully"""
    logger.warning("SIGINT or CTRL-C detected. Exiting gracefully")
    exit(0)

signal(SIGINT, sigint_handler)
