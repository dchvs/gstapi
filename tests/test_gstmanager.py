#!/usr/bin/env python3

import unittest

import gi

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except BaseException:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)

from gstreamer.gstmanager import GstManager


class GstManagerTests(unittest.TestCase):
    def setUp(self):
        self.GstManager = GstManager('videotestsrc ! fakesink')

    def test_make(self):
        self.assertIsInstance(
            GstManager.make('videotestsrc ! fakesink'),
            Gst.Pipeline)

    def test_start(self):
        self.GstManager.start()
        self.assertEqual(Gst.State.PLAYING, self.GstManager.get_state())

    def test_stop(self):
        self.GstManager.stop()
        self.assertEqual(Gst.State.NULL, self.GstManager.get_state())

    def test_get_state(self):
        self.assertIsInstance(self.GstManager.get_state(), Gst.State)
