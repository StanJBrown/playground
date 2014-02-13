#!/usr/bin/env python
import os
import sys
import time
import signal
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.config
import playground.benchmark.ssh_utils as ssh_utils

# SETTINGS
cwd = os.path.dirname(__file__)
# config_fp = os.path.normpath(os.path.join(cwd, "../config/grand_central.json"))


class SSHUtilsTests(unittest.TestCase):
    def test_test_connection(self):
        pass


if __name__ == '__main__':
    unittest.main()
