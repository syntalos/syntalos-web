---
title: D2. Creating a new Python Module
type: docs
---

These instructions exist to create a new Python module from scratch.
If you just want to run some custom Python code, using the existing [Python Script]({{< ref "/docs/modules/pyscript" >}})
module is a much easier solution.

## 1. Module Location

First, decide on a short, lower-case name for your module. The name will be the unique identifier
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

Ports are registered via the `SyntalosLink` object returned by `syl.init_link()`. Port registration must happen
when the script is started (i.e. inside `if __name__ == '__main__'` or at module-level),
so Syntalos can discover the port topology before trying to restore saved project connections:

```python
import sys
import syntalos_mlink as syl

def main() -> int:
    # Initialize the connection to Syntalos first.
    syLink = syl.init_link()

    # Register input and output ports via the link object.
    # This must happen before await_data_forever() is called.
    iport = syLink.register_input_port('frames-in', 'Frames', syl.DataType.Frame)
    oport = syLink.register_output_port('rows-out', 'Results', syl.DataType.TableRow)

    # ... register callbacks, then run the event loop
    syLink.await_data_forever()
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

The three arguments to each registration call are: the port **ID** (a short, unique string used to identify the port),
a human-readable **title** shown in the Syntalos GUI, and a **data type** constant from `syl.DataType`
(e.g. `syl.DataType.Frame`, `syl.DataType.TableRow`, `syl.DataType.IntSignalBlock`).

Please note that you might need to set additional port metadata depending on which modules you plan
to connect to. Some modules expect specific port metadata, e.g. the built-in
[Plot Time Series]({{< ref "/docs/modules/plot-timeseries" >}}) module (consult its documentation for details).

## 4. Write your code

After setting all metadata, it is time to actually write your module's code!
Open `mod-main.py` for a complete example. A Python module is structured around a `main()` entry point
that initializes the Syntalos link, registers ports and callbacks, then calls `syLink.await_data_forever()`
to hand over control to the built-in event loop (or `syLink.await_data()` if you need more control).

### Lifecycle callbacks

Register lifecycle callbacks on the `SyntalosLink` object before calling `await_data_forever()`:

```python
syLink.on_prepare = mod.prepare   # called before each run; return True to signal readiness
syLink.on_start   = mod.start     # called when acquisition begins
syLink.on_stop    = mod.stop      # called when the run ends (always called)
```

### Settings

Settings are stored and loaded by Syntalos as an opaque `bytes` object. Register two callbacks to
handle serialization and deserialization:

```python
# Called by Syntalos to serialize the module's settings (e.g. when a project is saved).
# Receives the base project directory as a string (in case the module needs to reference
# other files); must return settings as bytes.
syLink.on_save_settings = lambda base_dir: bytes(json.dumps(my_settings), 'utf-8')

# Called by Syntalos to restore previously saved settings.
# Receives the settings bytes and base project directory; return True on success.
syLink.on_load_settings = lambda data, base_dir: load_settings_from_bytes(data)
```

### Settings GUI

If your module has `show-settings` listed in its `features` in `module.toml`, Syntalos will call
`syLink.on_show_settings` when the user clicks the settings button. Register a zero-argument callable:

```python
syLink.on_show_settings = self._show_settings_dialog
```

Inside `_show_settings_dialog()`, draw a GUI using PyQt6 or PySide6 (recommended for visual
compatibility with the rest of the Syntalos UI) to let the user adjust settings.

Refer to the [syntalos_mlink Python API documentation]({{< ref "/docs/pysy-mlink-api" >}}) for a full
reference of all available methods and data types.

## 5. Test

If your module is located in one of Syntalos' recognized locations, it should now show up in the module list, along all other modules,
and you should be able to use it as normal and test its functions.
