#!/usr/bin/env python3

import unittest

import gi
from gi.repository import GLib

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except BaseException:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)

from ..gstmanager import GstManager


class GstManagerTests(unittest.TestCase):
    def setUp(self):
        self.GstManager = GstManager('videotestsrc ! fakesink')

    def test_make(self):
        GstManager.make('videotestsrc ! fakesink')

    def test_start(self):
        self.GstManager.start()
        self.assertEqual(Gst.State.PLAYING, self.GstManager.get_state())

    def test_stop(self):
        self.GstManager.stop()
        self.assertEqual(Gst.State.NULL, self.GstManager.get_state())
