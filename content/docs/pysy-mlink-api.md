---
title: Python Module API
type: docs
prev: docs/timesync-verification
---

Syntalos provides a Python API to easily build new modules. Python modules do not
run within the Syntalos process, and instead communicate with the main application
via an interface provided by the `syntalos_mlink` Python module.
This API can be used from either the *Python Script* module, or by
standalone modules that are written in Python entirely.

The Python interface is documented below.

{{< include "pysy_mlink_api_embed.fragment" >}}
