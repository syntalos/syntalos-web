---
title: Hardware support for Flatpak users
type: docs
prev: docs/setup/install
weight: 20
---

{{< callout type="info" >}}
This page is mainly for users of the Flatpak bundle, or users redirected here by Syntalos due to missing host-side
hardware support.
If you installed Syntalos from the Debian/Ubuntu repository, or built and installed it manually with its host
integration files, you usually do not need any additional hardware support package.
{{< /callout >}}

If you installed Syntalos via Flatpak, you may still need a small host-side support package.
Some hardware access (especially USB device access via `udev` rules) must be configured on the host system,
outside the Flatpak sandbox.
The package only adds host-side support files. It does not replace or conflict with using Syntalos as a Flatpak app.

The `syntalos-hwsupport_*_all.deb` package provides these host-side files for Debian/Ubuntu systems.
Without it, some modules may not detect or access devices reliably.

## When to install this package

Install the hardware support package if:

- Syntalos shows a warning about missing hardware support.
- A module reports missing permissions for USB hardware.
- Devices are visible on the system but do not work in Syntalos.

## Debian / Ubuntu

Install the package even if the main Syntalos app itself is installed from Flathub.
You can [download syntalos-hwsupport from here](https://syntalos.github.io/repo/debian/pool/stable/s/syntalos/).

Then install the downloaded package manually with:

```bash
sudo apt install ./syntalos-hwsupport_*_all.deb
```

After installation, unplug and replug affected USB devices.
If needed, reboot once to ensure all host rules are reloaded.

## Other Linux distributions

There is currently no equivalent package for non-Debian/Ubuntu distributions.

If you are comfortable with manual system integration, you can copy the relevant `udev` and related
host files manually.
If not, please file an issue and we can help you. For the future, a distribution-agnostic method
to install this support is planned.
