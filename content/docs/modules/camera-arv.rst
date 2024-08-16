---
title: Aravis Camera
---
.. image:: /images/modules-src/camera-arv/camera-arv.svg
   :width: 80
   :align: right

The "Aravis Camera" module supports any industrial camera that implements the
`GenICam® <https://www.emva.org/standards-technology/genicam/>`_ specification
(via the `Aravis <https://github.com/AravisProject/aravis>`_ implementation of it).


Usage
=====

Select a camera and the desired camera settings in the module settings.
When you load a Syntalos project with saved settings, depending on the camera, some settings
may fail to apply since sometimes settings have to be applied in a certain order and GenICam
does not specify the right order.
You will receive an error message if any setting could not be applied.

The module outputs time-synchronized frames.

To view the generated video, use a *Canvas* module.


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
       | ``has_color``: Boolean, Whether the output frames have color or are grayscale.
