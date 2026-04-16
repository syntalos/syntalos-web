---
title: D2. Creating a new Python Module
type: docs
---

These instructions exit to create a new Python module from scratch.
If you just want to run some custom Python code, using the existing [Python Script]({{< ref "/docs/modules/pyscript" >}})
module is a much easier solution.

## 1. Module Location

First, decice on a short, lower-case name for your modue. The name will be the unique identifier
for modules of your new type and must not be changed in future (or otherwise existing configurations might break).

If you are compiling Syntalos manually, you can add your new Python module directly to the source tree in
the `modules/` directory, and then add a new `subdir` directive for it to the toplevel
[modules/meson.build](https://github.com/syntalos/syntalos/blob/master/modules/meson.build) file.

Alternatively, you can also have Python modules loaded from your home directory. Syntalos will look
in the following locations:

* `~/.local/share/Syntalos/modules` for normal installations
* `~/.var/app/org.syntalos.syntalos/data/modules` if installed as Flatpak bundle

Any modules copied there will be automatically loaded.

## 2. Copy a Template

The easiest way to start building a new module is to copy a template to have any boilerplate present.
A minimal Python module exists in the form of [example-py](https://github.com/syntalos/syntalos/tree/master/modules/example-py).
Copy its directory to the location where you develop your module, and rename it to your chosen ID name.

## 3a. Adjust Metadata

Open the copied `module.toml` file in your new module directory:

```toml
[syntalos_module]
type = "python"

name = "Python Module Example"
description = "Example & template for a Syntalos Python module."
icon = "penrose-py.svg"

main = "mod-main.py"
use_venv = false

categories = ['sydevel', 'example']
features = ['show-settings']
```

Using the `name` and `description` fields, you can set a human-readable name and short description for your module.
The `icon` field denotes the filename of an icon file to visually represent your module relative to the module's root directory.
It is recommended to pick a vector graphic in SVG/SVGZ format here, but a PNG raster graphic will also work.

You can delete the `devel = true` field, as that hides the module by default and makes it only visible when Syntalos' developer
mode is active.

By specifying a Python file in `main`, you can select which Python file will be the main entrypoint for your module. By setting
`use_venv` to `true`, Syntalos will also run your module in its own virtual environment, and will install any Python dependencies
from a `requirements.txt` file in the module's folder.

## 3b. Register Ports in Python

Ports are registered in your Python script. Add calls to `syl.register_input_port()` and `syl.register_output_port()`
at **module level** (i.e. as top-level code, not inside any function), so Syntalos can discover the port topology as
soon as the script is loaded:

```python
import syntalos_mlink as syl

# Register input and output ports at module level.
# This must run unconditionally when the script is loaded.
syl.register_input_port('frames-in', 'Frames', 'Frame')
syl.register_output_port('rows-out', 'Indices', 'TableRow')
syl.register_output_port('frames-out', 'Marked Frames', 'Frame')
```

The three arguments to each call are: the port **ID** (used in `get_input_port` / `get_output_port`),
a human-readable **title** shown in the Syntalos GUI, and the **data type** ID.

Please note that you might need to set additional port metadata depending on which modules you plan
to connect to. Some modules expect specific port metadata, e.g. the built-in
[Plot Time Series]({{< ref "/docs/modules/plot-timeseries" >}}) module (consult its documentation for details).

## 4. Write your code

After setting all metadata, it is time to actually write your module's code!
Open `mod-main.py` for an example. The Python module has the same familiar `prepare()`, `start()`, `run()` and `stop()`
functions like a Python Script module, that Syntalos will call at the appropriate time.
Ports are also accessed the same way, and data is also submitted the same way. Refer to the [syntalos_mlink API documentation]({{< ref "/docs/pysy-mlink-api" >}})
for a full reference of all available methods.

In addition to the known methods, a Python module also has a `set_settings(settings: bytes)` and `change_settings(old_settings: bytes)`
entry point. The former is called before a run is started with the module's settings serialized as bytes, in order for them to be applied before
the run is launched.
The latter is invoked by the user wanting to change module settings. Syntalos will provide the old settings, and it is up to the module to
draw a GUI to enable the user to change any of its settings

The example module will draw a simple GUI using tkInter, but for visual compatibility with the rest of the Syntalos UI, using PyQt6 or PySide
is recommended.

## 5. Test

If your module is located in one of Syntalos' recognized locations, it should now show up in the module list, along all other modules,
and you should be able to use it as normal and test its functions.
