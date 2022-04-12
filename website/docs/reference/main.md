---
sidebar_label: main
title: main
---

## Gucker Objects

```python
class Gucker(QtWidgets.QWidget)
```

#### stream\_folder

```python
def stream_folder(subfolder: str = None, sleep_interval: int = 1, regexp: str = "(?P<magnification>[^x]*)x(?P<sample>[^_]*)__w(?P<channel_index>[0-9]*)(?P<channel_name>[^-]*)-(?P<wavelength>[^_]*)_s(?P<sample_index>[0-9]*)_t(?P<time_index>[0-9]*).TIF", experiment: ExperimentFragment = None, force_match=False) -> RepresentationFragment
```

Stream Tiffs in Folder

Streams Tiffs in the subfolder in the user directory that was specified.

**Arguments**:

- `folder` _str, optional_ - The subfolder name. Defaults to None.
- `sleep_interval` _int, optional_ - The sleep interval if we didnt find a new image. Defaults to 1.
- `regexp` _str, optional_ - A regular expression defining extraction of metadata. Defaults to None.
- `experiment_name` _str, optional_ - The newly created Experiment we will create. Defaults to random name.
- `force_match` _bool, optional_ - Do you force a match for the regexp?
  

**Returns**:

- `Representation` - [description]
  

**Yields**:

- `Iterator[Representation]` - [description]

