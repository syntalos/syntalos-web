---
title: Network Control Protocol
weight: 50
---

Syntalos can coordinate recording runs across several computers on the same local
network with applications that speak its network control protocol.
One machine acts as the **controller** and broadcasts synchronization
commands; all other machines are **listeners** that start and stop their own local
recordings in response.

This page covers the protocol specification for developers who want to integrate
external software with a Syntalos fleet.

For users, check out the [Network Control Tutorial]({{< ref "/tutorials/05_network-control" >}}) instead.


## Specification

The reference demo scripts in [`tools/netctl-demo/`](https://github.com/syntalos/syntalos/tree/master/tools/netctl-demo)
implement this protocol in Python.


### Transport

| Channel           | ZMQ pattern | Default port | Direction        |
|-------------------|-------------|--------------|------------------|
| Commands          | PUB / SUB   | 5556         | Controller → listeners |
| Feedback (ACKs)   | PUSH / PULL | 5557         | Listeners → controller |

The controller **binds** both ports.  Listeners **connect** to the controller's
address.

Every command message is a **two-frame** ZMQ multipart message:

```
Frame 0: b"sy.cmd"           (topic, ASCII)
Frame 1: <UTF-8 JSON object> (payload)
```

ACK messages are **single-frame** and sent over the PUSH socket.


### Common JSON fields

All messages (commands and ACKs) carry:

| Field    | Type   | Description                                       |
|----------|--------|---------------------------------------------------|
| `v`      | int    | Protocol version - currently `1`                  |
| `type`   | string | Message type (see below)                          |
| `sender` | string | Instance ID of the originator; used for filtering |
| `run_id` | string | UUIDv7 hex string that identifies the run         |


### Command: `prepare`

Broadcast by the controller before a run starts.  Listeners should apply the
provided parameters and prepare the run.

```json
{
  "v": 1,
  "type": "prepare",
  "sender": "rig-ctrl",
  "run_id": "019312ab-...",
  "project": "my-project",
  "subject_id": "M42",
  "subject_group": "control",
  "experiment_id": "novel-object-1"
}
```

| Field           | Type   | Description           |
|-----------------|--------|-----------------------|
| `project`       | string | Project name (if any) |
| `subject_id`    | string | Subject ID            |
| `subject_group` | string | Subject group         |
| `experiment_id` | string | Experiment ID         |

When everything is prepared and the listener is ready to start acquiring data,
it must send a `prepare` ACK.


### Command: `start`

Broadcast after the controller has received all required `prepare` ACKs and has
started its own master timer.

```json
{
  "v": 1,
  "type": "start",
  "sender": "rig-ctrl",
  "run_id": "019312ab-...",
  "ts_start_us": 1737000000123456
}
```

| Field         | Type | Description                                                        |
|---------------|------|--------------------------------------------------------------------|
| `ts_start_us` | int  | Controller wall-clock start, µs since Unix epoch (`system_clock`)  |

Each listener uses `ts_start_us` to align its master clock so that t = 0 is
shared across all machines.  Alignment requires synchronized system clocks (NTP/PTP).


### Command: `stop`

Broadcast when the controller's run ends (normally or due to failure).

```json
{
  "v": 1,
  "type": "stop",
  "sender": "rig-ctrl",
  "run_id": "019312ab-...",
  "success": true
}
```

| Field     | Type | Description           |
|-----------|------|-----------------------|
| `success` | bool | Whether run succeeded |


### ACK message

Listeners send ACKs on the PUSH socket.

```json
{
  "v": 1,
  "type": "ack",
  "sender": "rig-cam",
  "run_id": "019312ab-...",
  "ack_for": "prepare",
  "success": true
}
```

On failure, add an `"error"` field:

```json
{
  ...
  "success": false,
  "error": "Module 'camera' failed to initialize"
}
```

| Field     | Type   | Description                                      |
|-----------|--------|--------------------------------------------------|
| `ack_for` | string | `"prepare"`, `"start"`, or `"stop"`              |
| `success` | bool   | `true` if the operation succeeded                |
| `error`   | string | Human-readable error; only present on failure    |


#### ACK timing

| Phase     | When sent                                                                                                                                             |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `prepare` | After all modules have prepared and the engine is **ready to start its timer**. Sent immediately with `success=false` if the engine fails to prepare. |
| `start`   | Immediately on receipt.                                                                                                                               |
| `stop`    | After the listener's engine has fully stopped and all data has been written to disk.                                                                  |


### Run state machine

```
Controller                                 Listener(s)
──────────                                 ──────────
broadcast: PREPARE()                ──▶    receive PREPARE
  block: wait for N prepare-ACKs           [engine prepares all modules]
                                    ◀──    prepare-ACK  (success / fail)

broadcast: START(ts_start_us)       ──▶    receive START
  run starts locally                       align master timer to ts_start_us
                                    ◀──    start-ACK  (immediate)

  … run in progress …                      … run in progress …

broadcast: STOP()                   ──▶    receive STOP
  run stops locally                        [engine stops, data flushed]
                                    ◀──    stop-ACK
```

**Controller ACK handling:**

- **Prepare ACKs** - the controller blocks until it has received the expected
  number of ACKs (configurable) or times out.  A timeout or a negative ACK
  causes the controller to abort and broadcast `stop` so listeners can clean up.
- **Start ACKs** - collected passively; the run is not delayed waiting for them.
  If too few arrive within the timeout, an error is raised.
- **Stop ACKs** - informational; the controller does not wait for them.

**Listener timeout:**

If a listener does not receive the `start` command within 30 seconds of sending
its prepare ACK, it aborts its local run, sends a negative `prepare` ACK, and
resets to idle.


### Self-filter

Every instance ignores messages whose `sender` matches its own instance ID.  This
prevents an instance that has both controller and listener modes active from
acting on its own broadcasts.


### Versioning

Messages with `"v"` other than `1` are silently dropped.  Future protocol
versions will use a different `v` value and remain backwards-compatible at the
transport level.
