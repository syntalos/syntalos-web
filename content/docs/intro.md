---
title: Introduction
next: docs/setup/install
---

Acquisition of data from a variety of heterogeneous sources with precisely aligned timestamps is a requirement for many
kinds of in vivo experiments.
In addition, it is often necessary to manipulate experimental settings based on the animal's state or behavior,
and to store acquired data in a standardized format to simplify subsequent analysis.
To address these requirements, Syntalos exists.
It is capable of simultaneous acquisition of data from an arbitrary amount of sources,
including multi-channel electrophysiological recordings and different
types of live imaging devices.

At the same time, the program supports closed-loop, real-time interventions with
different actuators. Precisely matching timestamps for all inputs are ensured by continuous statistical analysis
and correction of the individual devices' timestamps and by use of the parallel-processing capabilities of
modern CPUs. New data sources can be integrated relatively easily as well, using Syntalos' module system.

All data generated from a given experiment is stored in a well-defined, comprehensive structure,
making it easy to compare, pool or share data between experimentalists with different research questions.
With these features, Syntalos enables reliable multi-modal recordings as well as closed-loop interventions
for many different (neuro)scientific questions.

## Design Goals

Syntalos was created with a specific set of goals in mind. Some of them are based on experiences gathered
during work on in vivo experiments with many animals and many different experimenters, others were derived
from experience with developing software that had similar requirements to Syntalos.

 * Timestamps of all data sources of an experiment should be synchronized (within tolerance limits), so data at
   specific points in time can be compared directly. If hardware synchronization is unavailable, a software solution
   should be used to achieve reasonable synchronization.
 * A data acquisition task must never block a different acquisition or processing task.
 * Data is stored in a fixed directory structure (Experiment Directory Layout, EDL) with all metadata alongside the data.
 * The software must account for experimenter error and have sane failure modes (autocorrect bad experimenter input, never
   have a component fail silently, warn about anticipated future issues (like low disk space), etc.).
 * The software must never auto-adjust parameters without at least logging the fact or alerting the user.
 * The software may use platform-specific features to achieve its design goals.
   Syntalos being written for Linux enables it to make use of some beneficial Linux-specific functionality
   to increase its robustness or performance.


## Architecture Overview

{{< callout type="info" >}}
This information is intended for curious readers and people who want to develop Syntalos itself
or develop new modules for it.
For the daily operation of the software and to simply use it, it is not required to understand
how it is designed.
{{< /callout >}}

### Module Integration & Operation

![Syntalos Process Design](/images/sydsgn/syinterop-design.png "Structure of the Syntalos process & module interactions")

Syntalos runs most of its modules in separate kernel threads, subjecting them to the scheduler of the operating system.
This ensures that modules within threads that do interface with hardware are never blocked by other tasks within the
bigger Syntalos process and can react to incoming hardware events quickly, especially if their threads are running at
elevated priority.

For modules that do not have such strict requirements, Syntalos is also able to employ event-based patterns to execute
module code, where multiple modules share one kernel thread.

Communication between modules happens via lock-free queues, ensuring data is passed between threads and within threads
both efficiently and safely.

For user-defined code, like Python scripts, Syntalos will spawn a separate process and communicate with it using efficient
and fast IPC (Inter-process communication) methods. This ensures that a crash in user-defined code will never result in
the whole Syntalos process crashing as well. It also allows, in case of Python, to have multiple Python modules in different
Python virtualenvs, increasing the versatility of custom Python modules.
Lastly, running this code as separate process means the main Syntalos process can interrupt and even forcefully kill misbehaving
modules, increasing robustness of the program. This is not possible with modules running in kernel threads.

If the latency and efficiency gains of a threaded module are not required, running a module using Syntalos' IPC interface is recommended.

### Module Lifecycle

![Syntalos Module Lifecycle](/images/sydsgn/symodule-lifecycle.png "State transitions of a Syntalos module")

Syntalos modules, when they are added to a board, run through an initialization phase first that is only executed once per module.
During which, they can set up essential data structures and configure themselves (Python modules may make sure their virtualenv exists
at that stage).

Once an experiment run is started, all modules execute a *Prepare* stage in sequence. During this stage they configure metadata, set up
their respective devices and perform any long-running other preparation steps in advance, before actually running. Once a module has completed
its preparations, it transitions to a *Ready* state. Once all modules are ready, the Syntalos engine will make all modules transition to a *Start*
stage in parallel. At that point the module is running and must complete any action in this stage as quickly as possible.

After starting, all modules are *Running* until the user stops the current experiment. Once an experiment is stopped, the Syntalos engine
transitions all modules into a *Stop* state in sequence, at which modules can finalize their processing and write any metadata.
At the end, Syntalos writes additional global metadata, ensures all modules have stopped safely, and then waits for another run to start.

### Organizational Components

Syntalos is split into 7 components with different purposes:

#### Public Interface Shared Libraries

**libsyntalos-datactl**: This shared library contains Syntalos' data type system and data management functions. It defines data types that can be
exchanged using data streams between modules (such as `Frame`, `IntSignalBlock`, etc.), as well as classes to write EDL data, *tsync* files and
time synchronization algorithms. It also contains the clock implementation of Syntalos and is used by all other components of the program.

**libsyntalos-mlink**: This shared library provides the "module link" interface implementation that allows users to create new out-of-process
Syntalos modules. It is the foundational building block for Syntalos Python integration, but also enabled the creation of Syntalos modules in
any other programming language that can interface with a C/C++ shared library.

#### Internal Libraries

**syntalos-fabric**: This library provides interfacing glue between the Syntalos main executable and shared-library modules. Modules link against
it to have access to internal Syntalos data structures and shared common code. Its interface is not stable and the library may only be used by modules
that are provided by Syntalos itself or that are intended for merging into the main Syntalos repository.

**syntalos-utils**: This library contains some common utility functions that are shared between modules and executables provided by Syntalos, to avoid
code duplication and speed up the build process of the Syntalos codebase.

#### Executables

**syntalos-roudi**: This executable provides an implementation of RouDi (Routing and Discovery) for the [Iceoryx](https://iceoryx.io/latest/) system
used by Syntalos for fast IPC. It holds the shared memory pools for inter-process data exchange and monitors all Syntalos modules that are using the
*mlink* interface to run in separate processes (as well as the Syntalos master process itself).

**pyworker**: This binary contains the Syntalos Python integration and makes use of the *mlink* glue code to communicate with the main Syntalos process.
It is spawned by the Syntalos master process for any Python module, and allows modules to be implemented in Python with ease and without C++ knowledge.

**syntalos**: The Syntalos main process itself which spawns all other processes. It contains the Syntalos engine as well as the graphical user interface.
