#!/usr/bin/env python3

import gi
from gi.repository import GLib

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except BaseException:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)


class GstManagerError(RuntimeError):
    pass


class GstManager:
    """
    Class that does the GStreamer operations.

    ...

    Attributes
    ----------

    Methods
    -------
    start()
        Start the GStreamer application.
    stop()
        Stop the GStreamer application.

    Raises
    ------
    GstManagerError
        This class custom exception.
    """

    def __init__(self):
        pass

    def start(self):
        """Start the GStreamer application.

        Parameters
        ----------

        Raises
        ------
        GstManagerError
            If unable to start the GStreamer application.
        """
        try:
            print("Starting the GStreamer application.")
        except BaseException:
            GstManagerError('Unable to start the GStreamer application')

    def stop(self):
        """Stop the GStreamer application.

        Parameters
        ----------

        Raises
        ------
        GstManagerError
            If unable to stop the GStreamer application.
        """
        try:
            print("Stopping the GStreamer application.")
        except BaseException:
            GstManagerError('Unable to stop the GStreamer application')
