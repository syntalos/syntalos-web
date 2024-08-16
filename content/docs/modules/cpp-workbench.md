---
title: C++ Workbench
---
<img class="align-right" src="/images/modules-src/cpp-workbench/cpp-workbench.svg" width="80px" />

Syntalos contains a powerful mechanism to safely write modules in any language and have them run
as a separate process, thereby making it safe to experiment without accidentally crashing the whole
Syntalos experiment.

Normally, you would write a module from scratch using the provided APIs and make it available to Syntalos.
The *C++ Workbench* module however wraps this support into an easy-to-use module, making it a lot
easier to experiment with it and write simple code.

## Usage

Syntalos needs access to a C++ compiler and the respective toolchain in order for this module to work.
Make sure the required components are installed.

{{< callout type="info" >}}
If you are **not** using the Flatpak build and are on a Debian-based Linux distribution, you
can install all required components via this command:
`sudo apt install gcc g++ pkgconf meson ninja-build`
{{< /callout >}}

Once you have written your C++ code, you can check if it compiles by clicking the *Compile Code* button.
When an experiment is started, Syntalos will also automatically compile your module for you and
launch it.

This permits using C++ as a scripting language just like Python.
If you make a mistake and your module crashes, it will not result in Syntalos itself crashing.
Your experiment run will fail, but the program itself will recover from these kinds of failures,
so you can correct your issue quickly.

Please keep in mind that this module is still a bit experimental and a proof-of-concept (but it
has been used successfully in real experiments, mainly to perform some fast computations that
were a bit too slow in Python).

The API description of the `SyntalosLinkModule` class that you implement when writing code for
this module can be found at
[Syntalos::SyntalosLinkModule]({{< ref "/api/classes/classsyntalos_1_1syntaloslinkmodule" >}}).

## Ports

* Ports are fully customizable via the *Port Editor*


## Stream Metadata

* Stream metadata is fully customizable in C++ code.


## Example Code

```cpp
#include <QCoreApplication>
#include <syntalos-mlink>

using namespace Syntalos;

class MyCppModule : public SyntalosLinkModule
{
    Q_GADGET
private:
    std::shared_ptr<OutputPortLink<TableRow>> m_tabOut;

public:
    explicit MyCppModule(SyntalosLink *slink)
        : SyntalosLinkModule(slink)
    {
        // Register some example ports
        m_tabOut = registerOutputPort<TableRow>("table-out", "Example Out");
        registerInputPort<TableRow>("table-in", "Example In", this, &MyCppModule::onTableDataReceived);
    }

    ~MyCppModule() = default;

    bool prepare(const QByteArray &) override
    {
        // Actions to prepare an acquisition run go here!

        // success
        return true;
    }

    void start() override
    {
        // Actions to perform immediately before data is first acquired go here
    }

    void onTableDataReceived(const TableRow &row)
    {
        // we just fast-forward the row without any edits to the output port
        m_tabOut->submit(row);
    }

    void stop() override
    {
        // Actions to perform once the run is stopped go here
    }
};

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    // Initialize link to Syntalos. There can only be one.
    auto slink = initSyntalosModuleLink();

    // Create & run module
    auto mod = std::make_unique<MyCppModule>(slink.get());
    slink->awaitDataForever();

    return a.exec();
}
```
