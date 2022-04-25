#!/usr/bin/env python3

from callbacks import supports_callbacks
from datetime import datetime
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


class GstRecordingError(RuntimeError):
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
            # GLib.MainLoop().run()
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
            # GLib.MainLoop().quit()
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
    appsrc : Gst.Element
        GStreamer AppSrc element instance.

    appsink : Gst.Element
        GStreamer AppSink element instance.

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
         Attributes
         ----------
         pulled_buffer : Gst.Buffer
            The GStreamer AppSink buffer bound for callbacks.

         Parameters
         ----------
         desc : str
            The GStreamer pipeline description.

        _gst_app : Gst.Pipeline
            The GStreamer application object.
         """

        super().__init__(desc)

        pipeline_index = self._gst_app.name.replace('pipeline', '')

        self.appsrc = self._gst_app.get_by_name('appsrc' + pipeline_index)
        self.appsink = self._gst_app.get_by_name('appsink' + pipeline_index)

        self.pulled_buffer = None
        self._pull_buffer_callback = None

    @supports_callbacks
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
            sample = self.appsink.emit('pull-sample')
            self.pulled_buffer = sample.get_buffer()
        except BaseException:
            raise GstManagerError(
                'Unable to pull the GStreamer buffer from Appsink.')

        print("@pull_buffer")
        # return Gst.FlowReturn.OK
        return self.pulled_buffer

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
            self.appsrc.emit('push-buffer', buffer)
        except BaseException:
            raise GstManagerError(
                'Unable to pull the GStreamer buffer from Appsrc.')

    def _install_pull_buffers_callback(self):
        """ Install the callback to AppSink to pull the buffers.

        Parameters
        ----------

        Returns
        -------

        Raises
        ------
        GstAppManagerError
            If unable to install the callback to AppSink to pull the buffers.
        """
        try:
            def _pull_buffer_callback(appsink=None, data=None):
                print("auch1!")
                self.pull_buffer()

                return Gst.FlowReturn.OK

            self._pull_buffer_callback = _pull_buffer_callback
            self._pull_buffer_callback.pull_buffer = self.pull_buffer
            # self._pull_buffer_callback, None) #
            self.appsink.connect(
                'new-sample', self._pull_buffer_callback, None)
        except BaseException:
            raise GstManagerError(
                'Unable to install the callback to AppSink to pull the buffers.')

    def _x(self, appsink=None, data=None):
        print("auch!")
        return Gst.FlowReturn.OK


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


class GstEvents(GstAppManager):
    """
    Class that handles GStreamer events.

    ...

    Attributes
    ----------

    Methods
    -------

    Raises
    ------
    GstRecordingError
        This class custom exception.
    """

    def __init__(self, desc):
        """
         Parameters
         ----------
         desc : str
         """
        super().__init__(desc)


class GstRecording(GstAppManager):
    """
    Class that does GStreamer recording operations.

    ...

    Attributes
    ----------

    Methods
    -------


    Raises
    ------
    GstRecordingError
        This class custom exception.
    """

    def __init__(self):
        """
         Parameters
         ----------
         """
        # videotestsrc num-buffers=10 is-live=true
        # appsrc is-live=true name=appsrc
        desc = 'appsrc is-live=true name=appsrc ! x264enc ! mpegtsmux ! filesink async=false location=dinitahouse_{time}.ts'.format(
            time=datetime.now().strftime("%d_%m_%Y_%I:%M:%S_%p"))
        super().__init__(desc)

    def make_recording(self) -> None:
        """Make the GStreamer buffer mapping.

        Parameters
        ----------

        Returns
        -------

        Raises
        ------
        GstRecordingError
            If unable to make the recording.
        """
        try:
            self.start()
        except BaseException:
            raise GstMapsError(
                'Unable to make the recording.')
