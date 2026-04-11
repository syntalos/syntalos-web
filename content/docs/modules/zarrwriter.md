---
title: Zarr Writer
---
<img class="align-right" src="/images/modules-src/zarrwriter/zarrwriter.svg" width="80px" />

This module writes timestamped matrix data into a [Zarr](https://en.wikipedia.org/wiki/Zarr_(data_format))
array store.

## Usage

Only one input datatype is accepted at a time, so you can connect either the `Float64 Signals` or the `Int32 Signals` input port,
but not both at the same time.

### Reading Data

It is recommended to load the generated data using the [edlio](https://edl.readthedocs.io/latest/)
Python module, which will do the right thing automatically.
You can also manually open the data and read it via any Zarr reader that supports Zarr v3.
Data will be stored in checksummed, zstd-compressed form, which is widely supported.

In Python, the [python-zarr](https://zarr.readthedocs.io/en/stable/) module is available to
read the array data.

## Ports

| Name             | Direction | Data Type          | Description         |
|------------------|-----------|--------------------|---------------------|
| 🠺Float64 Signals | In        | `FloatSignalBlock` | Float signal data   |
| 🠺Int32 Signals   | In        | `IntSignalBlock`   | Integer signal data |


## Stream Metadata

No output streams are generated, but for input streams of type `FloatSignalBlock`/`IntSignalBlock` the
following metadata will be handled explicitly:

| Key            | Type         | Required?   | Description                                       |
|----------------|--------------|-------------|---------------------------------------------------|
| `signal_names` | List<String> | Recommended | List of signal names contained in each data block |
| `sample_rate`  | Double       | Recommended | Sampling rate in samples per second.              |
| `time_unit`    | String       | No          | Unit of the data block timestamps.                |
| `data_unit`    | String       | No          | Unit of the signal block values.                  |
