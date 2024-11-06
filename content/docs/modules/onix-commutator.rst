---
title: ONIX Coax Commutator
---
.. image:: /images/modules-src/onix-commutator/onix-commutator.svg
   :width: 80
   :align: right


This module provides simple support for the `ONIX Coaxial Commutator <https://open-ephys.github.io/onix-docs/Hardware%20Guide/Commutators/index.html>`_
when fed quaternions from an orientation sensor.


Usage
=====

Set up the commutator hardware as described in their `guide <https://open-ephys.github.io/commutator-docs/coax-commutator/user-guide/mount-connect.html>`_.
After adding this module to your Syntalos experiment and connecting the hardware to your computer, select the right serial port in the module settings.

You will then have to connect a module providing unit quaternions (with the rotation information of your animal) to the `ONIX Commutator` module, so it
knows how to turn. Hardware that can generate this data is for example the BNO055 sensor on a Miniscope. The `Miniscope module <{{< ref "miniscope" >}}>`_
provides this data as output stream which can be connected to the `ONIX Commutator` module's input directly.


Ports
=====

.. list-table::
   :widths: 14 10 22 54
   :header-rows: 1

   * - Name
     - Direction
     - Data Type
     - Description

   * - 🠺Quaternions
     - In
     - ``FloatSignalBlock``
     - Unit quaternion vector input


Stream Metadata
===============

No output streams are generated. For the quaternion input stream, the ``signal_names`` metadata property must be
set to a string list containing the quaterion names "qw", "qx", "qy", "qz" in exactly this order.
The received vectors must have a length of 4 and contain the quaterions in this order.
