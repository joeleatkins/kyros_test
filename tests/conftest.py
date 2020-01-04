import logging
import os
import sys

import pytest

sys.dont_write_bytecode = True


def quiet_py4j():
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.INFO)
