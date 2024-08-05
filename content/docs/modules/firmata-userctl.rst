---
title: Firmata User Control
---
.. image:: /images/modules-src/firmata-userctl/firmata-userctl.svg
   :width: 80
   :align: right

This module can connect with any `Firmata I/O <{{< ref "firmata-io" >}}>`_ module to allow the user manual control
over the Firmata device.

Usage
=====

Add manual outputs and raw data display controls in the module's display panel.
Once an experiment is running, and the "Firmata User Control" is connected to a "Firmata IO" module
with both its ports, data can be read from and written to the device.

.. image:: /images/manual-firmata-control-dialog.avif
  :width: 480
  :alt: Manually reading Arduino pin values and writing to pins

See also:

* Tutorial: `Firmata Interface Tutorial <{{< ref "/tutorials/04_firmata-interface" >}}>`_

Ports
=====

.. list-table::
   :widths: 14 10 22 54
   :header-rows: 1

   * - Name
     - Direction
     - Data Type
     - Description

   * - 🠺Firmata Input
     - In
     - ``FirmataData``
     - Read data from a `Firmata Data` port of a Firmata IO module.
   * - Firmata Control🠺
     - Out
     - ``FirmataControl``
     - Write data to a `Firmata Control` port of a Firmata IO module.


Stream Metadata
===============

Default stream metadata.
