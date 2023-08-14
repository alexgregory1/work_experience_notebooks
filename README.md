# Work Experience Notebooks

## Setting up a Virtual Environment

Install miniforge which is an open source version of the conda package manager. The official install instructions can be found here https://github.com/conda-forge/miniforge#install. On Mac, you can install it using the following command.

```
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
bash Mambaforge-$(uname)-$(uname -m).sh
```

On windows you can install the installer from https://github.com/conda-forge/miniforge.

Check miniforge is installed correctly.

```
$ conda --version
conda 23.1.0
```

Navigate to somewhere sensible such as your documents directory.

```
$ cd ~/Documents
```

Clone or copy this repository onto your machine.

```
$ git clone git@gitlab.stfc.ac.uk:HDS/work_experience_notebooks.git
```

Navigate to the repository.

```
$ cd work_experience_notebooks
```

Create a conda environment called `census` and install the packages in `environment.yml`.

```
$ conda create -n census -f environment.yml
```

Activate the environment.

```
$ conda activate census
```

Check some of the packages are installed properly.

```
$ python3
Python 3.10.12 | packaged by conda-forge | (main, Jun 23 2023, 22:41:52) [Clang 15.0.7 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> import pandas as pd
>>> np.__version__
'1.25.2'
>>> pd.__version__
'2.0.3'
```

Start Jupyter Lab.

```
$ jupyterlab
```

