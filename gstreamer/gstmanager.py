#!/usr/bin/env python3

from callbacks import supports_callbacks
from datetime import datetime
from detectionapi.detection.detection import YoloV5_Supported_Shape
import logging
from typing import Tuple

import gi

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except BaseException:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)


time = datetime.now().strftime("%d_%m_%Y_%I:%M:%S_%p")

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

        # Enable to pull buffers when added a callback to it.
        if self.appsink is not None:
            self._install_pull_buffers_callback()

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

        logging.debug("pull_buffer: GstAppManager.pull_bufffer called.")
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
                self.pull_buffer()
                return Gst.FlowReturn.OK

            self._pull_buffer_callback = _pull_buffer_callback
            self._pull_buffer_callback.pull_buffer = self.pull_buffer

            self.appsink.connect(
                'new-sample', self._pull_buffer_callback, self.appsink)
        except BaseException:
            raise GstManagerError(
                'Unable to install the callback to AppSink to pull the buffers.')


class GstDict(dict):
    """
    Class that does represents a dictionary.

    ...

    Attributes
    ----------
    self : dict
        This dictionary instance.

    Methods
    -------
    insert(key : int, value : Any)
        Method to insert into dictionary.

    Raises
    ------
    """
    def __init__(self):
        self = dict()

    def insert(self, key, value):
        self[key] = value


class GstStreamHandler(GstDict):
    """
    Class that represents a dict. of GStreamer stream objects.

    ...

    Attributes
    ----------
    stream_dict : GstDict
        Dictionary instance to hold GStreamer stream objects.

    Methods
    -------
    insert(int : key, [Gst.Pipeline : gst_stream_obj | GstAppSinkManager : gst_stream_obj])
        Method to insert into dictionary the GStreamer stream object.

    Raises
    ------
    """
    def __init__(self):
        self.stream_dict = super()

    def insert(self, key, gst_stream_obj):
        self.stream_dict.insert(key, gst_stream_obj)


class GstAppSinkManager(GstManager):
    """
    Class that does the GStreamer operations for applications with fed buffers.

    ...

    Attributes
    ----------
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

        self.appsink = self._gst_app.get_by_name('appsink0')

        self.pulled_buffer = None
        self._pull_buffer_callback = None

        # Enable to pull buffers when added a callback to it.
        if self.appsink is not None:
            self._install_pull_buffers_callback()

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

        logging.debug("pull_buffer: GstAppManager.pull_bufffer called.")
        return self.pulled_buffer

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
                self.pull_buffer()
                return Gst.FlowReturn.OK

            self._pull_buffer_callback = _pull_buffer_callback
            self._pull_buffer_callback.pull_buffer = self.pull_buffer

            self.appsink.connect(
                'new-sample', self._pull_buffer_callback, self.appsink)
        except BaseException:
            raise GstManagerError(
                'Unable to install the callback to AppSink to pull the buffers.')


class GstAppSrcManager(GstManager):
    """
    Class that does the GStreamer operations for applications with fed buffers.

    ...

    Attributes
    ----------
    appsrc : Gst.Element
        GStreamer AppSrc element instance.

    Methods
    -------
    push_buffer()
        Push the GStreamer buffer from Appsink.

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

        self.appsrc = self._gst_app.get_by_name('appsrc0')

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
    def map_buffer(cls, buffer, map_flags) -> Tuple[bool, Gst.MapInfo]:
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
            map_buf_obj = buffer.get_all_memory()
            result, mapinfo = map_buf_obj.map(map_flags)

        except BaseException:
            raise GstMapsError(
                'Unable to make the GStreamer buffer mapping.')

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


class GstRecording(GstAppSrcManager):
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
        desc = (f'appsrc max-bytes=26035200 is-live=true do-timestamp=true format=3 '
            f' caps="video/x-raw,width={YoloV5_Supported_Shape.Width},height={YoloV5_Supported_Shape.Height},pixel-aspect-ratio=1/1,framerate=30/1,format=RGB"'
            f' ! videoscale ! videoconvert ! avenc_mpeg4 ! identity dump=false silent=true ! mpegtsmux ! queue ! filesink sync=false async=false qos=false location=dinitahouse_{time}.ts')

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
