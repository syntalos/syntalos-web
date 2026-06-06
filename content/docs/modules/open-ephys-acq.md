---
title: Open Ephys AcqBoard
---
<img class="align-right" src="/images/modules-src/open-ephys-acq/open-ephys-acq.svg" width="80px" />

This module streams electrophysiology data from the [Open Ephys Acquisition Board](https://open-ephys.org/acq-board) Gen2 and Gen3.
Check out [Differences Between Generations](https://open-ephys.github.io/acq-board-docs/User-Manual/Generations-differences.html)
to see which hardware you have.


## Usage

The settings dialog is split into three groups:

* **Backend** — choose between the real hardware
  (*Open Ephys Acquisition Board*), or *Simulated*. The currently active
  backend is displayed next to the selector; the **Reconnect** button
  re-probes the bus, which is useful after plugging the board in.
* **Acquisition** — sample rate (the available rates depend on the
  backend), and optional streaming of the per-headstage AUX channels
  (3 per headstage) and the board's eight on-board ADC inputs. The
  channel naming scheme (*Global index* `CH1, CH2, ...` versus
  *Stream-relative* `A1_CH1, A1_CH2, ...`) is also set here.
* **Headstages** — summary of currently detected headstages and their
  active channel counts. The **Measure impedances…** action runs the
  board's on-chip impedance scan and updates the per-channel readout.

Per-channel masking is available in the channel inventory: any channel
disabled there is dropped from the corresponding output port. During a
run, toggling a still-enabled channel mutes its column (zero-fill) for
the rest of the run — useful for isolating noisy channels live without
restarting acquisition.

The module also accepts a TTL trigger input port: connect an upstream
module that emits `LineCommand` events, and the module fires the
board's digital output lines accordingly. Only `WriteDigitalPulse`
commands on lines 0–15 are honoured; other command kinds are ignored.

### Wiring example

![Wiring example for the OpenEphys AcqBoard Module](/images/modules/openephys-acq-wiring1.avif)

The live plotted signals in a [Plot Time Series]({{< ref "plot-timeseries" >}}) module may look like this:

![Plotting example for the OpenEphys AcqBoard](/images/modules/openephys-acq-signalplot1.avif)


## Output Data Format

Sample data is published as `SignalBlockU16`. The
`data_unit` / `data_scale` / `data_offset` metadata keys describe how
to recover physical µV values — see [Common Stream Metadata]({{< ref "/docs/common-stream-metadata" >}})
for the contract. Display modules like
[Plot Time Series]({{< ref "plot-timeseries" >}}) apply the transform on the fly;
writer modules like [Zarr Writer]({{< ref "zarrwriter" >}}) persist the keys so
recordings can be converted to µV after the fact.

Each connected headstage produces up to two output ports:

* an *electrode* port, and
* an *AUX* port, when AUX streaming is enabled.

A single board-wide *ADC* port (`adc`) is published when ADC streaming
is enabled. Ports that would have zero enabled channels are not
registered. Ports that survive a rescan keep their identity, so live
subscriptions on other modules are unaffected when an unrelated
headstage is replugged.


## Ports

| Name                         | Direction | Data Type        | Description                                        |
|------------------------------|-----------|------------------|----------------------------------------------------|
| 🠺 TTL Triggers               | In        | `LineCommand`    | Digital pulses to fire on the board's TTL outputs. |
| Headstage *<prefix>* 🠺       | Out       | `SignalBlockU16` | Electrode samples for one headstage.               |
| Headstage *<prefix>* – AUX 🠺 | Out       | `SignalBlockU16` | AUX channels for one headstage (when enabled).     |
| Board ADC 🠺                  | Out       | `SignalBlockU16` | Data from the on-board ADC inputs (when enabled).  |
| TTL Input 🠺                  | Out       | `LineReading`    | Data from the on-board TTL inputs (when enabled).  |


## Stream Metadata

All output ports carry the
[standard signal-stream metadata]({{< ref "/docs/common-stream-metadata" >}}):

| Key            | Value                                                        |
|----------------|--------------------------------------------------------------|
| `sample_rate`  | The configured sample rate, in Hz.                           |
| `time_unit`    | Always `index`.                                              |
| `signal_names` | Per-channel labels in the configured naming scheme.          |
| `data_unit`    | `µV` (the unit after the affine transform).                  |
| `data_scale`   | The board's per-LSB conversion factor for this channel kind. |
| `data_offset`  | `0.0`.                                                       |
| `is_digital`   | `true`, only set for the digital TTL `LineReading` output.   |
