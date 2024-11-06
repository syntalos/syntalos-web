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

You need Ubuntu 24.04 or later in order to run Syntalos.
You can see your Ubuntu/Kubuntu version in the system settings,
usually under "Details".

### Add the PPA

Run these commands to add a software source for the pre-compiled version of Syntalos:
```bash
sudo add-apt-repository ppa:ximion/syntalos
sudo apt update
```

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

### Download the packages

Go to the [Syntalos Releases](https://github.com/syntalos/syntalos/releases) page and download
the .deb packages for your Debian version.

### Install Syntalos

You can install the packages using your graphical package manager (just make sure the
`syntalos-hwsupport*.deb` package is installed first).

Alternatively, you can extract the ZIP rchive to a directory and install the packages
from the command-line:
```bash
cd path/with/syntalos/debfiles
sudo apt install ./syntalos*.deb
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
