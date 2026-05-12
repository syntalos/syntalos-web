---
title: 04. Controlling simple devices
type: docs
next: D1_new-cpp-module
---

[Arduino](https://www.arduino.cc/) is an open-source microcontroller platform that,
when combined with the [Firmata](https://github.com/firmata/protocol) firmware, can
be used to easily control a variety of devices using its analog and digital output ports.

Anything that can be controlled using TTL pulses will work, and there are also other devices
and more specialized sensors that you can integrate.
We published instructions on how to build some of these devices
at [our Maze Hardware site](https://github.com/bothlab/maze-hardware/blob/main/README.md).

This tutorial will require some hardware tinkering and a bit of coding in Syntalos to be useful,
so it is for intermediate users.

{{< callout type="info" >}}
Starting with Syntalos 3.0, the Firmata-specific stream types were replaced by the
protocol-agnostic ``LineCommand`` / ``LineReading`` types and the matching
``HwOutputLine`` / ``HwInputLine`` Python convenience wrappers. If you are porting an existing
2.x project, see the [Syntalos 2.0 → 3.0 Porting Guide]({{< ref "/docs/porting-2to3" >}}).
{{< /callout >}}

## 1. Prepare your Arduino

Open your Arduino IDE. The navigate to *Sketch → Include Library → Manage Libraries*.
Search for *Firmata* and install the "Firmata by Firmata Developers" item.

![Installing Firmata for Arduino](/images/arduino-firmata-install.avif)

Then, navigate to *File → Examples → Firmata*, and select the Firmata variant you want. *Standard Firmata* is the
option we select here.

The Firmata code for Arduino opens in a window, and you can upload it to your device the usual way.
The Arduino is now ready to be used, so let's test it!

## 2. Set up Syntalos

Create a new Syntalos project and add a *Python Script*, *Firmata User Control*, *Firmata IO* and *Table* module.
Enter the settings of the Python module and edit its ports. Add a `firmata-in` input port with input data
type `LineReading` and an output port of type `LineCommand` named `firmatactl-out`.
You can also add an output port of type `TableRow` named `table-out` for later use.
The we create some boilerplate code for the Python module, which does nothing, for now:

```python
import syntalos_mlink as syl


fm_iport = syl.get_input_port('firmata-in')
fm_oport = syl.get_output_port('firmatactl-out')
tab_oport = syl.get_output_port('table-out')


def prepare() -> bool:
    """This function is called before a run is started.
    You can use it for (slow) initializations."""
    return True


def start():
    """This function is called immediately when a run is started.
    This function should complete extremely quickly."""
    pass


def stop():
    """This function is called once a run is stopped."""
    pass
```

To play around with Firmata manually, without using the script yet, we connect input and output of *Firmata User Control*
to the respective ports of *Firmata IO*:

![Using an Arduino with Firmata manually in Syntalos](/images/syntalos-firmata-manual-config.avif)

Open the settings of *Firmata IO* and select the serial port number of your plugged-in Arduino.

{{< callout type="info" >}}
If the device does not show up for selection or you get a permission error upon launching your experiment,
you may need to add yourself to the `dialout` group to use serial devices.
In order to do that, open a terminal and enter `sudo adduser $USER dialout`, confirming with
you administrator password. After a reboot / relogin, connecting to your Arduino should work now.
{{< /callout >}}

## 3. Manual work

Before automating anything, we want to run some manual tests first and control our Arduino by hand.
For testing purposes, we wire up an LED to one of its free ports.
We can then already hit the *Ephemeral Run* button of Syntalos, to start a run without saving any data.

Double-click on the `Firmata User Control` module to bring up its display window. There, you can read
inputs and write to outputs. Click on the *Plus* sign to add a new *Manual Output Control* and add
a digital output pin.
On the *Received Input* side, select an analog, or digital input. Select the Arduino pins that you want to read
or write from, and change the values of your output.
The Arduino should react accordingly, and also display the read input values.

![Manually reading Arduino pin values and writing to pins](/images/manual-firmata-control-dialog.avif)

This is pretty nice already, but we do want to automate this, so Syntalos can change values automatically,
for example based on test subject behavior, and also write the data it reads to a file for later analysis.

## 4. Automation: Blinking light

To automate things, we need to go back to the Python script again.
First, we need to break the port connections between *Firmata User Control* and *Firmata IO* (select them
with a click, and then push the *Disconnect* button), and instead connect the ports to the respective
*Python Script* ports:

![Using an Arduino with Firmata controlled by a Python script in Syntalos](/images/syntalos-firmata-pyscript-config.avif)

For demonstration purposes, we will let an LED blink at a given interval first, and log the time
when we sent the command to get the LED to blink.

This is the code we need to achieve that:

```python {linenos=table,hl_lines=[10,20,29,38]}
import syntalos_mlink as syl


# constants
LED_DURATION_MSEC = 250
LED_INTERVAL_MSEC = 2000


fm_iport = syl.get_input_port('firmata-in')
fm_oport = syl.get_output_port('firmatactl-out')
tab_oport = syl.get_output_port('table-out')

# pin 8 is wired to our LED; OutputLine just captures the identity, it does
# not emit any command on construction.
led = syl.HwOutputLine(fm_oport, line_id=8)


def prepare() -> bool:
    # set table header and save filename
    tab_oport.set_metadata_value('table_header', ['Time', 'Event'])
    tab_oport.set_metadata_value('data_name_proposal', 'events/led_status')

    return True


def start():
    # configure pin 8 as a digital output on the Firmata device. This must
    # be called at the start of every run.
    led.send_mode()

    # start sending our pulse command periodically
    trigger_led_pulse()


def trigger_led_pulse():
    tab_oport.submit([syl.time_since_start_msec(),
                      'led-pulse'])
    led.pulse(LED_DURATION_MSEC)

    if not syl.is_running():
        return False

    # run this function again after some delay
    syl.schedule_delayed_call(LED_INTERVAL_MSEC, trigger_led_pulse)


def stop():
    # ensure LED is off once we stop
    led.set_value(False)
```

In line 11, we fetch references to our input/output ports (using only the latter for now), so we
can use them in later parts of the script. We then construct a `HwOutputLine` (line 15) that ties the
LED's hardware line ID to our control output port. Construction is cheap and does not emit anything —
it only captures identity.

The `prepare()` function is called before the experiment run is actually started.
In it we can set metadata on our respective ports. In our case we set a table header using the `table_header`
property on the table row output port, and also suggest a name to save the resulting CSV table under using
the `data_name_proposal` property.

Then, once the experiment is started, we configure the LED line as an output on the Firmata device by
calling `led.send_mode()`. **This must be done at the start of every run** — Firmata IO clears its
internal pin table between runs, so prior registrations do not survive.

{{< callout type="info" >}}
``HwOutputLine`` is a convenience wrapper. The equivalent low-level call is:

```python
ctl = syl.new_line_command(syl.LineCommandKind.SET_MODE, line_id=8)
ctl.flags = syl.LineModeFlags.IS_OUTPUT
fm_oport.submit(ctl)
```
Not every action has convenience methods, but the most common operations do.
{{< /callout >}}

Then, we launch our custom function `trigger_led_pulse()` where the actual logic happens to make the LED blink.
In it, we send a new table row to the *Table* module for storage & display, using the `syl.time_since_start_msec()` function
to get the current time since the experiment run was started and naming the event `led-pulse`. You should see these two values
show up in the table later. Then, we actually send a command to the *Firmata IO* module to instruct it to set the LED pin `HIGH`
for the time `LED_DURATION_MSEC`.

To introduce some delay before sending another such command, we instruct the `trigger_led_pulse()` function to be called again
after `LED_INTERVAL_MSEC` via `syl.schedule_delayed_call(LED_INTERVAL_MSEC, trigger_led_pulse)`.
This is repeated until the experiment has been stopped by the user.

{{< callout type="warning" >}}
Keep in mind that when submitting data on a port, you are **not** calling the respective task immediately - you are
merely enqueueing an instruction for the other module to act upon at a later time.
Realistically, Syntalos will execute the queued action instantly with little delay, but Syntalos can not make any
real-time guarantees for inter-module communication.
If you need those, consider using dedicated hardware or an FPGA, and control those components with Syntalos instead.
This will give you predictable and reliable latencies.
{{< /callout >}}

If you hit the *Run* button, the experiment should run and the LED should blink for 250 msec every 2 sec.

## 5. Automation: Reading Data

Now, let's read some data and let an LED blink for each piece of data that was received!
We assume you have a switch placed on one Arduino pin, and an LED on another for testing purposes.

The code we need for this looks very similar to our previous one:

```python {linenos=table,hl_lines=[14,15,30,39,45]}
import syntalos_mlink as syl


# constants
LED_DURATION_MSEC = 500


fm_iport = syl.get_input_port('firmata-in')
fm_oport = syl.get_output_port('firmatactl-out')
tab_oport = syl.get_output_port('table-out')

# Hardware-line handles. Construction captures port + line_id; we call
# send_mode() in start() to configure the lines at the start of each run.
switch = syl.HwInputLine(fm_oport, line_id=7)
led    = syl.HwOutputLine(fm_oport, line_id=8)


def prepare() -> bool:
    # set table header and save filename
    tab_oport.set_metadata_value('table_header', ['Time', 'Event'])
    tab_oport.set_metadata_value('data_name_proposal', 'events/led_status')

    # call a function once new data was received on this input port
    fm_iport.on_data = on_new_line_reading

    return True


def start():
    switch.send_mode()
    led.send_mode()


def on_new_line_reading(data):
    if data is None:
        return

    # we only want to look at the 'switch' pin
    if data.line_id != switch.line_id:
        return

    if data.value:
        tab_oport.submit([syl.time_since_start_msec(),
                            'switch-on'])
        led.pulse(LED_DURATION_MSEC)
    else:
        tab_oport.submit([syl.time_since_start_msec(),
                            'switch-off'])


def stop():
    # ensure LED is off once we stop
    led.set_value(False)
```

In `start()` we now register both lines: pin `7` as an input (the switch) and pin `8` as an output (the LED).
We also need to read input from our Firmata device now, for which we registered `fm_iport` as input port.
Every input port in Syntalos' Python interface has an `on_data` property which you can assign a custom function to,
to be called when new data is received. We assign our own `on_new_line_reading()` function in this example.

In `on_new_line_reading()`, we first check if the received `data` is valid (it may be `None` to signal that a run
is being stopped right now). Next, we match the reading against the switch's line ID by comparing `data.line_id`
to `switch.line_id`. Since the input port can in principle carry readings from any line, this match is what tells us
the reading came from our switch.
Then, if we receive a `True` value, we command the LED to blink for half a second and log that fact in our table, otherwise
we just log the fact that the switch is off.

Upon running this project, you should see the LED flash briefly once you push the button, and see the state of the button logged
in the table displayed by the *Table* module.

## 6. Expansion

With this, you have basic control over a lot of equipment to control behavior experiments, from TTL-controlled lasers,
to gates and lick sensors.
Try making this work with your hardware, try [some DIY Maze Hardware](https://github.com/bothlab/maze-hardware/blob/main/README.md)
or hardware from other open source projects to make behavior experiments work.
