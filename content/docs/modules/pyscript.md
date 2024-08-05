---
title: Python Script
---
<img class="align-right" src="/images/modules-src/python.svg" width="80px" />

The "Python Script" module provides Syntalos' Python scripting interface.
It allows users to write custom Python code to control experiment behavior.


## Usage

You can enter custom Python script in the modules' *Settings* window and add/remove input
and output ports using the port editor (reachable via *Ports → Edit* in the script main window):

![An EDL directory tree](/images/pyscript-ports-dialog.avif "The ports configuration dialog")

There are tutorials available that explain how to use this module:

* [Script Control Tutorial]({{< ref "/tutorials/03_script-control" >}})
* [Firmata Interface Tutorial]({{< ref "/tutorials/04_firmata-interface" >}})

## Ports

* Ports are fully customizable using the port editor.


## Stream Metadata

* Stream metadata is fully customizable by scripting.


## Example Script

This is an example script that just demonstrates how to obtain video from
an input port, and just forwards the data to its output port without editing it.
It also outputs the timestamp when it received a new frame:

```python
import syntalos_mlink as syl


# Get references to your ports by their ID here.
# Examples:
iport_frame = syl.get_input_port('frame-in')

oport_frame = syl.get_output_port('frame-out')
oport_tab = syl.get_output_port('tablerow-out')


def prepare():
    """This function is called before a run is started.
    You can use it for (slow) initializations.
    NOTE: You are *not* able to send output to ports here, or access
    any valid master timer time. This function can be slow."""

    # set function to call when new data is received
    iport_frame.on_data = on_new_frame_data

    # set table output metadata
    oport_tab.set_metadata_value('table_header', ['Time Received', 'Frame Time'])
    oport_tab.set_metadata_value('data_name_proposal', 'events/table')


def start():
    """This function is called immediately when a run is started.
    Access to the timer is available, and data can be sent via ports.
    You can *not* change any port metadata anymore from this point onward.
    This function should be fast, many modules are already running at this point."""

    # copy the framerate from input to output
    oport_frame.set_metadata_value('framerate', iport_frame.metadata['framerate'])
    oport_frame.set_metadata_value_size('size', iport_frame.metadata['size'])


def on_new_frame_data(frame):
    # output a frame row with the timestamps
    oport_tab.submit([syl.time_since_start_usec(), frame.time_usec])

    # forward the received frame
    oport_frame.submit(frame)


def run():
    """This function is called once the experiment run has started."""

    # wait for new data to arrive and communicate with Syntalos
    while syl.is_running():
        syl.await_data()


def stop():
    """This function is called once a run is stopped, by the user, and error or when
    the loop() function returned False."""
    pass
```
