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

{{% detailsicon title="Installation on Ubuntu" closed="true" %}}

{{% steps %}}

### Verify the Ubuntu version

You need Ubuntu 24.04 or later in order to run Syntalos.

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

{{% /steps %}}

{{% /detailsicon %}}

{{% detailsicon title="Other Linux / Software Store" closed="true" %}}

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

{{% /steps %}}

{{% /detailsicon %}}


