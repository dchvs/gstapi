#!/usr/bin/env python3

import unittest

from ..gstmanager import GstManager


class GstManagerTests(unittest.TestCase):
    def setUp(self):
        self.GstManager = GstManager()

    def test_start(self):
        self.GstManager.start()

    def test_stop(self):
        self.GstManager.stop()
