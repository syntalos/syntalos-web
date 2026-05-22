---
title: Syntalos 2.x → 3.0 Porting
type: docs
weight: 35
---

Syntalos 3.0 contains a small number of **breaking changes** that affect projects
authored against the 2.x series. This page summarizes what changed and how to
migrate existing setups.


## At a glance

- Stream types are now protocol-agnostic: `LineCommand` / `LineReading` replace
  `FirmataControl` / `FirmataData`.
- Hardware addressing in `Line*` is ID-based only: `line_id` replaces `pin_id` +
  `pin_name`.
- Python port helper APIs for `Line*` are redesigned as `syl.HwOutputLine` / `syl.HwInputLine`.
- Signal block types are renamed to include their precision, and `SignalBlockF32` is now a 32-bit float.
- The "Firmata User Control" (`firmata-userctl`) module has been renamed to "Manual Line Control" (`hwline-userctl`)


## 1. Porting Python modules & PyScript scripts

### Port types

Anywhere your Python module's port editor had **`FirmataControl`** or
**`FirmataData`** selected, switch to **`LineCommand`** / **`LineReading`**.

### Replacing the convenience helpers

The 2.x API put convenience methods directly on `OutputPort`:
`firmata_register_digital_pin`, `firmata_submit_digital_value`,
`firmata_submit_digital_pulse`. All three are **removed** in 3.0. In their
place, two small Python classes — `HwOutputLine` and `HwInputLine` — capture
the identity of a hardware line and expose the operations valid for it.

**Before (2.x):**

```python
import syntalos_mlink as syl

oport_fm = syl.get_output_port('firmatactl-out')

def start():
    # register two pins
    oport_fm.firmata_register_digital_pin(7, 'switch', is_output=False, is_pullup=True)
    oport_fm.firmata_register_digital_pin(8, 'led1', is_output=True)

def trigger():
    oport_fm.firmata_submit_digital_pulse('led1', duration_msec=50)
    oport_fm.firmata_submit_digital_value('led1', False)
```

**After (3.0):**

```python
import syntalos_mlink as syl

oport_fm = syl.get_output_port('firmatactl-out')

# Capture identity once. Construction is side-effect-free.
switch = syl.HwInputLine(oport_fm, line_id=7, pullup=True)
led    = syl.HwOutputLine(oport_fm, line_id=8)

def start():
    # Explicitly register at every run
    switch.send_mode()
    led.send_mode()

def trigger():
    led.pulse_msec(duration_msec=50)
    led.set_value(False)
```

Notes:

- **`send_mode()` must be called at the start of every run.**
  Constructing the `HwOutputLine` / `HwInputLine` once in
  module scope and re-registering in `start()` is the recommended pattern.
- The `line_id` is the only identity — there is no `pin_name` anymore.
  If you used names to disambiguate readings, match on
  `reading.line_id == my_line.line_id` instead.
- `HwOutputLine(port, line_id, analog=True)` exposes `set_analog_value(code)`
  for DAC-style outputs. Calling `set_value` or `pulse` on an analog line
  (or `set_analog_value` on a digital line) raises a clear `SyntalosPyError`.

### Reading line readings

Field renames in the inbound type:

| 2.x               | 3.0                                                                 |
|-------------------|---------------------------------------------------------------------|
| `data.pin_id`     | `data.line_id`                                                      |
| `data.pin_name`   | *removed* — match `data.line_id` against your `HwInputLine.line_id` |
| `data.is_digital` | *removed* — the receiver already knows                              |
| `data.value`      | `data.value` (now an unsigned 32-bit integer)                       |

**Before (2.x):**

```python
def on_new_firmata_data(data):
    if data is None or not data.is_digital:
        return
    if data.pin_name != 'switch':
        return
    handle_switch(data.value)
```

**After (3.0):**

```python
def on_new_line_reading(data):
    if data is None:
        return
    if data.line_id != switch.line_id:
        return
    handle_switch(data.value)
```

### Low-level constructors

| 2.x                                                   | 3.0                                            |
|-------------------------------------------------------|------------------------------------------------|
| `syl.new_firmatactl_with_id_name(kind, pin_id, name)` | `syl.new_line_command(kind, line_id, value=0)` |
| `syl.new_firmatactl_with_id(kind, pin_id)`            | `syl.new_line_command(kind, line_id, value=0)` |
| `syl.new_firmatactl_with_name(kind, name)`            | *removed* — use `line_id`                      |

Most user code should not need these; `HwOutputLine` / `HwInputLine` cover the
common operations. If you construct raw commands, note that line setup is now
`LineCommandKind.SET_MODE` plus `LineModeFlags`:

```python
cmd = syl.new_line_command(syl.LineCommandKind.SET_MODE, line_id=8)
cmd.flags = syl.LineModeFlags.IS_OUTPUT
oport_fm.submit(cmd)
```

Pulse durations live in `cmd.duration_usec`; `cmd.value` is only the line value
or analog code. Device-specific payloads use `cmd.extra` together with
`syl.LineCommandKind.DEVICE_SPECIFIC`.


## 2. Stream data type changes

### Signal block type renames

All signal block data types have been renamed for clarity and to reflect their
exact bit width:

| 2.x                 | 3.0              |
|---------------------|------------------|
| `FloatSignalBlock`  | `SignalBlockF32` |
| `IntSignalBlock`    | `SignalBlockI32` |

This affects C++ type names, Python classes such as `syl.SignalBlockF32()`, and
the Python `syl.DataType.*` constants.
The `SignalBlockU16` is new in 3.0 and has no 2.x equivalent.

### Float precision change

The precision of `SignalBlockF32` (formerly `FloatSignalBlock`) has changed from
`double` (64-bit) to `float` (32-bit).
This has some algorithmic advantages and matches what many DAQ systems output.
Both `SignalBlockI32` and `SignalBlockF32` are now consistently 32-bit, which
also allows further signal block types to be added more easily in the future.

Reach out to us if you have a use case that needs higher-precision floating point
numbers as a stream data type!
