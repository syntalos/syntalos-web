---
title: Common Stream Metadata
weight: 10
---

Every Syntalos data stream carries a small key/value map of static metadata
alongside the actual samples. Producers set the keys that are meaningful
for their data; consumers default gracefully when a key is absent.

The keys themselves are not enforced types - they are conventions shared
across modules. This page is the canonical list. Module pages refer back
to it where they handle a specific key.

## Routing metadata

These keys are set automatically by Syntalos on every output stream and
are intended for downstream provenance / data-naming. Modules don't
normally read or write them directly.

| Key                  | Type   | Description                                                      |
|----------------------|--------|------------------------------------------------------------------|
| `src_mod_type`       | String | Type (unique identifier) of the source module.                   |
| `src_mod_name`       | String | User-defined name of the source module instance.                 |
| `src_mod_port_title` | String | Title of the source module's output port.                        |
| `data_name_proposal` | String | Proposed name for the dataset that stores data from this stream. |


## Signal / sample streams

For one-dimensional time-series streams (`SignalBlockU16`,
`SignalBlockI32`, `SignalBlockF32`).

| Key            | Type           | Default        | Description                                                                                                  |
|----------------|----------------|----------------|--------------------------------------------------------------------------------------------------------------|
| `sample_rate`  | Double (Hz)    | —              | Sampling frequency. Required when `time_unit` is `index`, recommended otherwise.                             |
| `time_unit`    | String         | `milliseconds` | One of `index`, `seconds`, `milliseconds`, `microseconds`. Describes the per-sample timestamps.              |
| `signal_names` | List\[String\] | —              | Per-channel labels. The list length must match the channel count.                                            |
| `data_unit`    | String         | —              | Physical unit of a sample *after* the affine transform below is applied (e.g. `µV`, `mPa`, `°C`).            |
| `data_scale`   | Double         | `1.0`          | See `data_offset`.                                                                                           |
| `data_offset`  | Double         | `0.0`          | Together with `data_scale`, defines the affine relation between raw samples on the wire and physical values. |


### The `data_unit` / `data_scale` / `data_offset` contract

Consumers that want physical-unit values apply

```
physical_value = data_scale * raw_value + data_offset
```

and interpret the result as being in the unit named by `data_unit`. The
defaults (`scale = 1.0`, `offset = 0.0`) make this a no-op for streams
that already carry physical-unit samples, so producers that emit
pre-scaled data only need to set `data_unit`.

Two patterns are common:

* **Pre-scaled** (e.g. [Intan RHX]({{< ref "modules/intan-rhx" >}})): samples arrive
  as `float32` already in µV. The module sets `data_unit = "µV"` and
  leaves `data_scale` / `data_offset` unset (i.e. identity).
* **Raw + transform** (e.g. [Open Ephys AcqBoard]({{< ref "modules/open-ephys-acq" >}})):
  samples stay as `uint16` to minimize bandwidth and storage. The
  module sets `data_unit = "µV"`, `data_scale`, and
  `data_offset`.

Writers ([Zarr Writer]({{< ref "modules/zarrwriter" >}}), [JSON Writer]({{< ref "modules/jsonwriter" >}}))
persist the keys alongside the raw data so the conversion is recoverable
even after a recording is closed.


## Image / frame streams

For `Frame` streams.

| Key         | Type        | Description                                            |
|-------------|-------------|--------------------------------------------------------|
| `framerate` | Double (Hz) | Frame rate.                                            |
| `size`      | `MetaSize`  | Frame dimensions in pixels (width × height).           |
| `has_color` | Bool        | True if frames carry colour data, false if monochrome. |


## Table-row streams

For `TableRow` streams.

| Key            | Type           | Description                                                       |
|----------------|----------------|-------------------------------------------------------------------|
| `table_header` | List\[String\] | Column names. The list length must match each row's column count. |
