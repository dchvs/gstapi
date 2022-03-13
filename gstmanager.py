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
    """

    def __init__(self):
        pass

    def start(self) -> None:
        """Start the GStreamer application.

        Parameters
        ----------

        Raises
        ------
        """
        print("Starting the GStreamer application.")

    def stop(self) -> None:
        """Stop the GStreamer application.

        Parameters
        ----------

        Raises
        ------
        """
        print("Stopping the GStreamer application.")
