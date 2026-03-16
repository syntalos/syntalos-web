---
title: Download Syntalos
toc: false
---

## Release Information

{{< cards >}}
  {{< card link="/docs/setup/install/" title="Installation Instructions" icon="download" >}}
  {{< card link="changes" title="Release Notes" icon="newspaper" >}}
{{< /cards >}}


## Quick Install Guides

<!--
##############
UBUNTU & KUBUNTU
##############
-->
{{% detailsicon title="Installation on Ubuntu & Kubuntu" icon="images/distros/ubuntu.svg" closed="true" %}}

{{% steps %}}

### Verify the Ubuntu version

You need Ubuntu 24.04 or later in order to run Syntalos. To run the latest version
of Syntalos, we recommend Ubuntu 26.04.
You can see your Ubuntu/Kubuntu version in the system settings,
usually under "Details".

### Add the repository

Run this setup command in a terminal to set up the software source for Syntalos on Ubuntu:
```bash
curl -fsSL https://raw.githubusercontent.com/syntalos/repo/refs/heads/main/publish/setup-syntalos-repo.sh | sudo sh
```

The script will add an APT repository source to your system. You can
[inspect the source code](https://github.com/syntalos/repo/blob/main/publish/setup-syntalos-repo.sh)
of the script to see exactly what it does.

### Install Syntalos

```bash
sudo apt install syntalos
```

### Allow the current user access to serial devices

```bash
sudo usermod -a -G dialout $USER
```

{{% /steps %}}

{{% /detailsicon %}}


<!--
##############
DEBIAN
##############
-->
{{% detailsicon title="Installation on Debian" icon="images/distros/debian.svg" closed="true" %}}

{{% steps %}}

### Verify the Debian version

We are currently building packages for Debian 13 (Trixie).
You can see your Debian version in the system settings dialog,
or run `cat /etc/os-release` in a terminal to see it.

### Add the repository

Run this setup command in a terminal to set up the software source for Syntalos on Debian:
```bash
curl -fsSL https://raw.githubusercontent.com/syntalos/repo/refs/heads/main/publish/setup-syntalos-repo.sh | sudo sh
```

The script will add an APT repository source to your system. You can
[inspect the source code](https://github.com/syntalos/repo/blob/main/publish/setup-syntalos-repo.sh)
of the script to see exactly what it does.

### Install Syntalos

```bash
sudo apt install syntalos
```

### Allow the current user access to serial devices

```bash
sudo usermod -a -G dialout $USER
```

{{% /steps %}}

{{% /detailsicon %}}


<!--
##############
FLATPAK & OTHER
##############
-->
{{% detailsicon title="Other Linux / Software Store" icon="images/distros/linux.svg" closed="true" %}}

{{% steps %}}

### Ensure Flathub is set up

Make sure that Flatpak and Flathub are configured on your system.
For many Linux distributions, this is already the case, but you can find
instructions on how to set up the software source [on the Flatpak website](https://flatpak.org/setup/).

### Install Syntalos

Install Syntalos either graphically by searching for it in your software
installer application (GNOME Software, KDE Discover, etc.), or from
the command-line using this command:
```bash
flatpak install flathub org.syntalos.syntalos
```

### Allow the current user access to serial devices

```bash
sudo usermod -a -G dialout $USER
```

{{% /steps %}}

{{% /detailsicon %}}
