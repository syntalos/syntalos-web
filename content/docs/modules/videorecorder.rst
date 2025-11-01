---
title: Video Recorder
---
.. image:: /images/modules-src/videorecorder/videorecorder.svg
   :width: 80
   :align: right

Record a stream of frames as video.


Usage
=====

This module has a multitude of settings to configure the recording and select a good balance between quality and speed.

It also permits encoding to be deferred to after the experiment run, to save resources for data acquisition during a run
(this will require a lot of disk space temporarily, so ensure you have enough space available).


FAQ
===

Which codec do I choose?
------------------------

That depends on what kind of data you record. But here is a general rule of thumb:

* If your data analysis needs precise measurements in post-processing and you must store exactly what the
  recording device produced in a pixel-perfect way (e.g. for Miniscope recordings), choose the **FFV1** codec.
* If you need accurate data, but pixel-perfection is not important, and you want great compatibility with
  applications that process video, choose the **VP9** codec.
* If your data analysis pipeline is modern, you can try using the **AV1** codec, which offers much better
  compression ratios and is suitable for lossless and non-lossless encoding.

{{< callout type="info" >}}
Remember to perform a test recording and play with the *Quality* or *Bitrate* settings for lossy codecs
to get the optimal result: A high-quality recording at the lowest-possible filesize.
{{< /callout >}}


Which container format do I choose?
-----------------------------------

Always choose `MKV` - it is widely supported, modern, and can hold newer codecs and additional metadata
that Syntalos adds to the video files. The `AVI` option exists only for compatibility with older data
analysis pipelines.


Should I use video file slicing?
--------------------------------

You generally don't need to slice the video recording into multiple parts, especially not if you
use the `MKV` container format.

You may will want to enable this feature if your offline data analysis pipeline does not have optimal
memory management and wants to load the entire video into memory. This can become an issue if the individual
video is large.

You may also want to enable this feature if your recording is extremely long (multiple hours) to increase
robustness in case of an error that could corrupt the video file.


Should I use the "Encode after run" option?
-------------------------------------------

The "Encode after run" feature is very powerful if your computer can not encode the video data while
the experiment is running. It will cause the video to be stored as raw data, and encoded into the selected
video file after the run. This also frees a lot of system resources for the experiment run.
Before anebling it though, you should consider the following things:

* Do you actually need to store all of this data? You may be able to live-encode your video stream if
  you scale down the size of the frames or crop them before storing them to disk. Just put a
  `Video Transformer <{{< ref "/docs/modules/videotransform" >}}>`_ in front of the Video Recorder
  to preprocess the frames.
* Can you select a different codec that your system may handle better?
  Maybe selecting a different bitrate or quality setting will help performance? Play around!
* If you choose to encode after the run, keep in mind that during the run, data is store **raw**.
  Unencoded video data is **extremely large**! Make sure that before using this option, you not only
  have sufficient amunts of free disk space for the raw recording available, but also enough space to
  store the encoded video alongside the raw video. Syntalos will only delete the original raw video copy
  after it was encoded successfully. Keep this in mind!
  Disk space has to be available in the data target directory (where the experiment data will be stored).


Ports
=====

.. list-table::
   :widths: 14 10 22 54
   :header-rows: 1

   * - Name
     - Direction
     - Data Type
     - Description

   * - 🠺Control
     - In
     - ``ControlCommand``
     - | ``STOP``: Stops recording and creates a new file.
       | ``START``: Resume recording, creating a new file if stopped, resuming the current file if paused.
       | ``PAUSE``: Pauses the current recording, does not create a new file.
       | ``STEP``: Encode one frame, then revert to the previous state (useful in combination with ``PAUSE``).
   * - 🠺Frames
     - In
     - ``Frame``
     - The frames to record.


Stream Metadata
===============

None generated (no output ports).
