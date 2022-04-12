#!/usr/bin/env python3

from typing import Tuple

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


class GstAppManagerError(RuntimeError):
    pass


class GstMapsError(RuntimeError):
    pass


class GstManager:
    """
    Class that does the GStreamer operations.

    ...

    Attributes
    ----------
    gst_app : Gst.Pipeline
        The GStreamer application object.

    Methods
    -------
    make()
        Make the GStreamer application object.
    start()
        Start the GStreamer application.
    stop()
        Stop the GStreamer application.
    get_state():
        Getter for the Gstreamer application state.

    Raises
    ------
    GstManagerError
        This class custom exception.
    """

    def __init__(self, desc):
        """
         Parameters
         ----------
        _gst_app : Gst.Pipeline
            The GStreamer application object.
         """
        Gst.init(None)

        self._gst_app = self.make(desc)

    @classmethod
    def make(cls, desc):
        """Make the GStreamer application process.

        Parameters
        ----------
        desc : str
            The description of the application process to make.

        Returns
        -------
        gst_app : Gst.Pipeline
            The GStreamer application object.

        Raises
        ------
        GstManagerError
            If unable to make the GStreamer application process.
        """
        try:
            gst_app = Gst.parse_launch(desc)
        except BaseException:
            raise GstManagerError(
                'Unable to make the GStreamer application process.')

        return gst_app

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
            self._gst_app.set_state(Gst.State.PLAYING)
            GLib.MainLoop().run()
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
            self._gst_app.set_state(Gst.State.NULL)
            GLib.MainLoop().quit()
        except BaseException:
            GstManagerError('Unable to stop the GStreamer application')

    def get_state(self):
        """Getter for the Gstreamer application state.

        Parameters
        ----------

        Returns
        -------
        state : Gst.State
            The GStreamer application state.

        Raises
        ------
        """
        state = self._gst_app.get_state(Gst.CLOCK_TIME_NONE)[1]
        return state


class GstAppManager(GstManager):
    """
    Class that does the GStreamer operations for applications with fed buffers.

    ...

    Attributes
    ----------

    Methods
    -------
    pull_buffer()
        Pull the GStreamer buffer from Appsink.

    Raises
    ------
    GstAppManagerError
        This class custom exception.
    """

    def __init__(self, desc):
        """
         Parameters
         ----------
         desc : str
            The GStreamer pipeline description.

        _gst_app : Gst.Pipeline
            The GStreamer application object.
         """

        super().__init__(desc)

    def pull_buffer(self):
        """ Pull the GStreamer buffer from Appsink.

        Parameters
        ----------

        Returns
        -------
        buffer : Gst.Buffer
            The GStreamer application buffer.

        Raises
        ------
        GstAppManagerError
            If unable to pull the GStreamer buffer from Appsink.
        """
        try:
            self.appsink = self._gst_app.get_by_name('appsink')
            sample = self.appsink.emit('pull-sample')
            buffer = sample.get_buffer()
        except BaseException:
            raise GstManagerError(
                'Unable to pull the GStreamer buffer from Appsink.')

        return buffer

    def push_buffer(self, buffer):
        """ Push the GStreamer buffer to Appsrc.

        Parameters
        ----------
        buffer : Gst.Buffer
            The GStreamer application buffer.

        Returns
        -------

        Raises
        ------
        GstAppManagerError
            If unable to push the GStreamer buffer to Appsrc.
        """
        try:
            self.appsrc = self._gst_app.get_by_name('appsrc')
            self.appsrc.emit('push-buffer', buffer)
        except BaseException:
            raise GstManagerError(
                'Unable to pull the GStreamer buffer from Appsrc.')


class GstMaps:
    """
    Class that does GStreamer mapping operations.

    ...

    Attributes
    ----------

    Methods
    -------
    map_buffer(Gst.Buffer : buffer)
        Make the GStreamer buffer mapping.

    Raises
    ------
    GstMapsError
        This class custom exception.
    """

    def __init__(self):
        """
         Parameters
         ----------
         """

    @classmethod
    def map_buffer(cls, buffer) -> Tuple[bool, Gst.MapInfo]:
        """Make the GStreamer buffer mapping.

        Parameters
        ----------
        buffer : Gst.Buffer
            The GStreamer buffer to map.

        Returns
        -------
        result, mapinfo : Tuple[bool, Gst.MapInfo]
            Mapping success result and map info with data mapped for reading.

        Raises
        ------
        GstMapsError
            If unable to make the GStreamer buffer mapping.
        """
        try:
            result, mapinfo = buffer.map(Gst.MapFlags.READ)

        except BaseException:
            raise GstMapsError(
                'Unable to make the GStreamer buffer mapping.')

        finally:
            buffer.unmap(mapinfo)

        return result, mapinfo
