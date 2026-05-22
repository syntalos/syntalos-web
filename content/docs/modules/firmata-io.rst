---
title: Firmata I/O
---
.. image:: /images/modules-src/firmata-io/firmata-io.svg
   :width: 80
   :align: right

This module can connect with any device speaking the `Firmata Protocol <https://github.com/firmata/protocol>`_ via
a serial port.


Usage
=====

Configure as usual by setting a serial device to connect to.

.. note::
    If the device does not show up for selection or you get a permission error,
    you may need to add yourself to the ``dialout`` group to use serial devices.
    In order to do that, open a terminal and enter ``sudo adduser $USER dialout``, confirming with
    you administrator password. Then log in again.

This module needs another module to be useful.

Example wiring for manually controlling a Firmata device and reading values from it:

.. image:: /images/modules/firmata-manual-control-wiring.avif
  :height: 300
  :alt: Syntalos wiring for manually reading from / writing to a Firmata device


Ports
=====

.. list-table::
   :widths: 14 10 22 54
   :header-rows: 1

   * - Name
     - Direction
     - Data Type
     - Description

   * - 🠺Line Control
     - In
     - ``LineCommand``
     - Hardware-line commands (set mode, write digital, pulse, ...) routed to the Firmata device.
   * - Line Readings🠺
     - Out
     - ``LineReading``
     - Timestamped scalar readings from the Firmata device's input pins.


Stream Metadata
===============

Default stream metadata.
