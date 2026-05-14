---
title: Miniscope
---
.. image:: /images/modules-src/miniscope/miniscope.svg
   :width: 80
   :align: right

This module provides support for recording data with `UCLA Miniscope <https://github.com/Aharoni-Lab/Miniscope-v4>`_ devices.
(This sometimes also includes industrial cameras for which no specialized drivers exist).


Usage
=====

Configure as usual.
Please ensure that when recording data, the raw frames are recorded and the displayed frames are displayed in a `Canvas`,
and not the other way round! Otherwise the recorded data may be incomplete.

.. image:: /images/miniscope-module-connections.avif
  :width: 340
  :alt: Miniscope connection diagram.


Ports
=====

.. list-table::
   :widths: 14 10 22 54
   :header-rows: 1

   * - Name
     - Direction
     - Data Type
     - Description

   * - Orientation Vector🠺
     - Out
     - ``SignalBlockF32``
     - Returns the orientation sensor quaternions (qw, qx, qy, qz) as vector.
   * - Orientation Rows🠺
     - Out
     - ``TableRow``
     - Returns the orientation sensor quaternions (qw, qx, qy, qz) as table rows. Includes acquisition timestamps as well.
   * - Display Frames🠺
     - Out
     - ``Frame``
     - Frames for display. Includes indicators and online background subtraction, as well as other user changes.
   * - Raw Frames🠺
     - Out
     - ``Frame``
     - Raw frames as recorded by the Miniscope.


Stream Metadata
===============

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Name
     - Metadata

   * - Orientation Vector🠺
     - | ``time_unit``: String, Unit of the timestamps. Always set to "milliseconds".
       | ``data_unit``: String, Unit of the signal block values. Set to "au".
       | ``signal_names``: List<String>, List of the quaterion names: "qw", "qx", "qy", "qz"
   * - Orientation Rows🠺
     - | ``table_header``: String List, Table header
   * - Display Frames🠺
     - | ``framerate``: Double, frame rate in FPS.
   * - Raw Frames🠺
     - | ``framerate``: Double, frame rate in FPS.
