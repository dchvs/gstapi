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

from gstapi.gstreamer.gstmanager import GstManager, GstAppManager


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


class GstAppManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.GstAppManager = GstAppManager(
            'videotestsrc ! appsink name=appsink')
        self.GstAppManager.start()

    def test_pull_buffer(self) -> None:
        buffer = self.GstAppManager.pull_buffer()
        self.assertIsInstance(buffer, Gst.Buffer)
