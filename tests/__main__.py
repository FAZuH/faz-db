import unittest
import sys

from loguru import logger

from tests.db.repository import TestWorldsRepository


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWorldsRepository)
    logger.debug(suite.countTestCases())
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=2)
    runner.run(suite)
