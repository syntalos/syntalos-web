---
title: Table
---
<img class="align-right" src="/images/modules-src/table.svg" width="80px" />

The "Table" module displays and saves any tabular content.


## Usage

No configuration required for now.
Data is saved unconditionally into a sanitized CSV table.

It is recommended to load the generated data using the [edlio](https://edl.readthedocs.io/latest/)
Python module, but you can also manually open the data and read it.
For example, using Pandas in Python:

```python
import pandas as pd

df = pd.read_csv('/path/to/data.csv', sep=';')
print(df)
```


Ports
=====

| Name     | Direction | Data Type  | Description                         |
|----------|-----------|------------|-------------------------------------|
| 🠺Rows   | In         | `TableRow` | Table rows to display and save.     |


Stream Metadata
===============

None generated (no output ports).
