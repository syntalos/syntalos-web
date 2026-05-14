---
title: Syntalos 2.x → 3.0 Porting
type: docs
weight: 35
---

Syntalos 3.0 contains a small number of breaking changes that affect projects
authored against the 2.x series. This page summarizes what changed and how to
migrate existing setups.

## Overview of breaking changes

| Area                            | 2.x                                      | 3.0                                            |
|---------------------------------|------------------------------------------|------------------------------------------------|
| Stream type                     | `FirmataControl`                         | `LineCommand`                                  |
| Stream type                     | `FirmataData`                            | `LineReading`                                  |
| Command-kind enum               | `FirmataCommandKind`                     | `LineCommandKind`                              |
| Pin-mode flags                  | implicit fields (`isOutput`, `isPullUp`) | `LineModeFlags` bitfield                       |
| Hardware addressing             | `pinId` (uint8) + `pinName` (string)     | `lineId` (uint16)                              |
| Pulse duration                  | `value` field (ms)                       | `duration` field (`microseconds_t`)            |
| Python — convenience helpers    | `OutputPort.firmata_*` methods           | `syl.HwOutputLine` / `syl.HwInputLine` classes |
| Python — low-level constructors | `syl.new_firmatactl_with_id_name` etc.   | `syl.new_line_command`                         |

The motivation: the old type names tied Syntalos's stream system to one
specific microcontroller protocol. Other devices (Open-Ephys digital I/O,
DAQ TTL outputs, custom stim hardware) deal in the exact same conceptual
shape — "set output X on hardware channel Y, optionally for time Z" — but
required Firmata-specific naming to participate. The 3.0 types are
protocol-agnostic; modules that emit or consume them work against any
backend that implements the line semantics.

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

fm_oport = syl.get_output_port('firmatactl-out')

def start():
    # register two pins
    fm_oport.firmata_register_digital_pin(7, 'switch', is_output=False, is_pullup=True)
    fm_oport.firmata_register_digital_pin(8, 'led1', is_output=True)

def trigger():
    fm_oport.firmata_submit_digital_pulse('led1', duration_msec=50)
    fm_oport.firmata_submit_digital_value('led1', False)
```

**After (3.0):**

```python
import syntalos_mlink as syl

fm_oport = syl.get_output_port('firmatactl-out')

# Capture identity once. Construction is side-effect-free.
switch = syl.HwInputLine(fm_oport, line_id=7, pullup=True)
led    = syl.HwOutputLine(fm_oport, line_id=8)

def start():
    # Explicitly register at every run
    switch.send_mode()
    led.send_mode()

def trigger():
    led.pulse(duration_msec=50)
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
| `data.value`      | `data.value` (now an integer up to 2^32)                            |

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
common operations. The standalone constructor is still useful when you need
a raw `LineCommand` (for example to fill in `extra` for a
`DeviceSpecific` payload).


## 2. Stream data type changes

### Signal block type renames

All signal block data types have been renamed for clarity and to reflect their
exact bit width:

| 2.x                 | 3.0              |
|---------------------|------------------|
| `FloatSignalBlock`  | `SignalBlockF32` |
| `IntSignalBlock`    | `SignalBlockI32` |
| `UInt16SignalBlock` | `SignalBlockU16` |

This affects both C++ code and the Python `syl.DataType.*` constants.

### Float precision change

The precision of `SignalBlockF32` (formerly `FloatSignalBlock`) has changed from
`double` (64-bit) to `float` (32-bit).
This has some algorithmic advantages and matches what most DAQ systems output.
Both `SignalBlockI32` and `SignalBlockF32` are now consistently 32-bit, which
also allows further signal block types to be added more easily in the future.
