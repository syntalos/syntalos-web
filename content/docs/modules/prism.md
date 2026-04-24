---
title: Prism
---
<img class="align-right" src="/images/modules-src/prism/prism.svg" width="80px" />

The Prism module splits color image frames into separate channel streams, combines
single-channel streams back into one color frame, or converts color frames to
grayscale.

## Usage

Prism has three operating modes:

### Split

Accepts one incoming frame stream and produces one single-channel output stream for
each enabled color channel.

This is useful if you want to process red, green, blue or alpha data independently.
Enabled channels can be selected in the module settings. By default, `Red`, `Green`
and `Blue` are enabled, while `Alpha` is disabled.

### Combine

Accepts one input stream per enabled channel and merges them into a single output
frame stream.

All input streams should be synchronized and have the same image size.
The output frame is emitted once data from every enabled and connected channel
has been received. If no alpha channel is enabled and connected, the generated frame
will contain only red, green and blue data.

### Grayscale

Accepts one color frame stream and converts it to a single-channel grayscale stream.

If the input is already single-channel, it is forwarded unchanged. BGR and BGRA input
frames are converted using OpenCV's grayscale conversion.

## Ports

The available ports depend on the selected mode and active channels.

### Split Mode

| Name       | Direction | Data Type | Description                                   |
|------------|-----------|-----------|-----------------------------------------------|
| 🠺Frames In | In        | `Frame`   | Multi-channel input frames                    |
| Red🠺       | Out       | `Frame`   | Single-channel red plane output               |
| Green🠺     | Out       | `Frame`   | Single-channel green plane output             |
| Blue🠺      | Out       | `Frame`   | Single-channel blue plane output              |
| Alpha🠺     | Out       | `Frame`   | Single-channel alpha plane output, if enabled |

### Combine Mode

| Name      | Direction | Data Type | Description                            |
|-----------|-----------|-----------|----------------------------------------|
| 🠺Red      | In        | `Frame`   | Single-channel red input, if enabled   |
| 🠺Green    | In        | `Frame`   | Single-channel green input, if enabled |
| 🠺Blue     | In        | `Frame`   | Single-channel blue input, if enabled  |
| 🠺Alpha    | In        | `Frame`   | Single-channel alpha input, if enabled |
| Combined🠺 | Out       | `Frame`   | Merged color output frame              |

### Grayscale Mode

| Name       | Direction | Data Type | Description                     |
|------------|-----------|-----------|---------------------------------|
| 🠺Frames    | In        | `Frame`   | Color or grayscale input frames |
| Grayscale🠺 | Out       | `Frame`   | Single-channel grayscale output |

## Stream Metadata

Prism forwards basic frame-stream metadata to its outputs.

For input streams of type `Frame`, the following metadata is handled explicitly:

| Key         | Type     | Required?   | Description                                  |
|-------------|----------|-------------|----------------------------------------------|
| `framerate` | Double   | Recommended | Frame rate in frames per second.             |
| `size`      | 2DSize   | Yes         | Frame dimensions in pixels.                  |

In `Split` and `Grayscale` mode, output metadata is copied from the single input
stream.

In `Combine` mode, the `Combined` output stream takes its `framerate` and `size`
metadata from the first connected input channel.
