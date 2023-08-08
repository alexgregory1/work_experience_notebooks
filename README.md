# Work Experience Notebooks

## Setting up a Virtual Environment

Create a virtual environment.

```
$ python3 -m venv .venv
```

Activate your virtual environment.

```
$ source .venv/bin/activate
```

Pip install the packages in `requirements.txt`.

```
$ pip install -r requirements.txt
```

Check that the packages have been installed.

```
$ python3
>>> import numpy as np
>>> import pandas as pd
>>> import matlotlib
>>> np.__version__
'1.25.2'
>>> pd.__version__
'2.0.3'
>>> matplotlib.__version__
'3.7.2'
```

Start JupyterLab.

```
$ jupyter lab
```
