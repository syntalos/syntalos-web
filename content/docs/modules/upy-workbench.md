---
title: MicroPython Workbench
---
<img class="align-right" src="/images/modules-src/upy-workbench/upy-workbench.svg" width="80px" />

The "MicroPython Workbench" module allows for relatively seamless integration of Syntalos
with microcontrollers running the [MicroPython](https://micropython.org/) firmware.


## Usage

You need to flash a microcontroller with MicroPython to get started. A cheap and capable option is using a
[Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html).

## Ports

* A custom number of input ports for `TableRow` tabular data can be registered.
* Data can be retrieved either as tabular `TableRow` data, `FloatSignalBlock` or `IntSignalBlock`

Input/output ports can be configured in the port editor.


## Stream Metadata

* All stream metadata are set to default values.


## Example Script

This is an example script that demonstrates how to use async code on the microcontroller
and pass messages between the device and Syntalos.

If the microcontroller does not need to receive data from Syntalos, the async code
can be replaced by sync code instead.


```python
import machine
from machine import Pin

ledPin = Pin('LED', Pin.OUT)
testPin = Pin(10, Pin.OUT)
sy = SyntalosCommunicator()


async def blink_led():
    oport_f = sy.get_output_port('float-out')
    while True:
        # send some numbers to the host, with the device timestamp
        timestamp = sy.ticks_ms()
        await oport_f.send_data([0.5, 1 if timestamp % 2 else 0], timestamp_ms=timestamp)

        # toggle the LEDs
        ledPin.high()
        testPin.low()
        await uasyncio.sleep(0.5)
        ledPin.low()
        testPin.high()
        await uasyncio.sleep(0.5)


def on_table_row_received(data):
    # just print any received table row to the console
    print('Received row:', data)


async def main():
    # Enable reading incoming data from the host
    sy.enable_input()

    # Blink a LED
    uasyncio.create_task(blink_led())

    # Receive tabular input
    sy.register_on_input('table-in', on_table_row_received)

    # Run this program indefinitely
    while True:
        await uasyncio.sleep(1)


# Run the main coroutine
uasyncio.run(main())
```

## Syntalos Interface API

You can interface with the Syntalos communication API primarily through the `SyntalosCommunicator` class,
which allows for an easy way to pass (text)data between Syntalos and the microcontroller.

{{< include "../upy_sycomm_api_embed.fragment" >}}
