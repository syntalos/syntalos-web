---
title: Tips & Tricks
prev: intro
next: modules/_index
---

This page contains semi-random tips and tricks that came up while using Syntalos and that other
experimenters may run into, but that do not necessarily warrant their own page.

### USB hardware fails / is slow if I plug in many USB devices

This is a very common issue especially if you are using many USB cameras simultaneously.
For cameras specifically, you can try switching to a different mode of connection,
for example using them via ethernet if the camera support GigE.

If you *need* to use USB, the cause of the issues is usually that multiple USB ports share the same USB
controller on commodity hardware. This means that despite multiple USB ports being available,
the potential maximum bandwidth (and sometimes even power) is split between them.
Syntalos can visualize which USB controllers your devices are connected to, so you can
redistribute them to ports where controllers are not shared. Click on *Diagnostics → USB Devices*
to get a list (and even more detailed information if USBView is installed).

If this does not help, and your problem is power, a powered USB hub can help in some rare
cases. If that is not the problem or does not help, adding a USB expansion card always solved
the issue so far.
Ideally, buy a card which has dedicated controllers for each USB port - those are a lot more
expensive than regular USB expansion cards, but are worth the money for scientific applications.

We had very good experience with the [StarTech.com 4-Port USB PCIe Card with 4X Independent USB Controllers](https://www.amazon.com/dp/B0DCKC11JM)
card (link points to its Amazon page).
