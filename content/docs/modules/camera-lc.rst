---
title: Camera
---
.. image:: /images/modules-src/camera-lc/camera-lc.svg
   :width: 80
   :align: right

The "Camera" module uses the modern `libcamera <https://libcamera.org/>`_ library to connect to
webcam-like camera devices.
This should work for standard USB UVC webcams, as well as more embedded cameras on devices such
as the Raspberry Pi.

For features ``libcamera`` does not yet support, the module will try to talk
directly to the `V4L2 API <https://en.wikipedia.org/wiki/Video4Linux>`_ to make them available
(needed for e.g. powerline frequency control).


Usage
=====

Configure as usual.


Ports
=====

.. list-table::
   :widths: 14 10 22 54
   :header-rows: 1

   * - Name
     - Direction
     - Data Type
     - Description

   * - Video🠺
     - Out
     - ``Frame``
     - ~


Stream Metadata
===============

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Name
     - Metadata

   * - Video🠺
     - | ``size``: 2D Size, Dimension of generated frames
       | ``framerate``: Double, Target framerate per second.
