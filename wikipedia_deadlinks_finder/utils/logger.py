from logging import getLogger, StreamHandler, INFO
from sys import stdout

logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(StreamHandler(stdout))
