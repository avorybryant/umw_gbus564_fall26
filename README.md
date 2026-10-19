# GBUS 564: Predictive Analytics — Coursework

Notebooks, datasets, and the shared helper package for GBUS 564 (Fall 2026).
Each week under `notebooks/` has:

- `notebooks/weekN/lectures/` — walkthrough notebooks covered in lecture
- `notebooks/weekN/assignments/` — the graded assignment notebook

## Running in Colab (recommended)

Every notebook has an **Open in Colab** badge at the top — click it to run in
the browser with no local setup. The first code cell installs this repo's
helper package:

```
pip install -q git+https://github.com/avorybryant/umw_gbus564_fall26.git
```

That package only needs `numpy`, `pandas`, and `scikit-learn`, so on Colab it
reuses the preinstalled libraries rather than upgrading them.

## Running locally

First, clone the repo and move into it:

```
git clone https://github.com/avorybryant/umw_gbus564_fall26.git
cd umw_gbus564_fall26
```

Then set up an environment with either uv or Anaconda.

### With uv

This repo is managed with [`uv`](https://docs.astral.sh/uv/) (Python 3.12+):

```
uv sync
uv run jupyter lab
```

`uv sync` installs the helper package plus everything the notebooks import
(TensorFlow/Keras, XGBoost, SHAP, statsmodels, …).

### With Anaconda

If you already have [Anaconda](https://www.anaconda.com/download) or
Miniconda, make a dedicated environment for the course rather than installing
into `base`. Run these from a terminal (on Windows, the **Anaconda Prompt**):

```
conda create -n gbus564 python=3.12
conda activate gbus564

python -m pip install --upgrade pip
pip install -e . --group notebooks
```

`pip install -e .` installs the course helper package from your local
checkout; `--group notebooks` adds everything the notebooks import (it needs
pip 25.1 or newer, hence the upgrade step). Install with `pip` inside the conda
environment rather than `conda install` — TensorFlow and SHAP are published to
PyPI first, and mixing the two installers in one environment is a common
source of broken imports.

Then start Jupyter from the same activated environment:

```
jupyter lab
```

If you'd rather launch Jupyter from **Anaconda Navigator** or another
Jupyter install, register the environment as a kernel once and pick
**Python (gbus564)** from the kernel menu:

```
python -m ipykernel install --user --name gbus564 --display-name "Python (gbus564)"
```

Each new session, run `conda activate gbus564` before `jupyter lab`. The
`%pip install` line at the top of every notebook is meant for Colab; locally
it just reinstalls the helper package from GitHub, which is harmless but can
be skipped.

### Getting new notebooks

Notebooks are added to this repo as the term goes on, so pull before starting
each week's work, then re-run your install step to pick up any helper-package
or dependency changes (it's a quick no-op when nothing changed):

```
git pull
uv sync                                  # uv
pip install -e . --group notebooks       # Anaconda (with gbus564 activated)
```

Restart any open Jupyter kernels afterwards so they load the updated package.

`git pull` will refuse to overwrite a notebook you've edited if that same
file was also updated here. To avoid that, do your work in a copy (e.g.
**File → Save Notebook As…** with your name in the filename) and leave the
original untouched.

## What's in the package

`src/gbus564_coursework/` is installed as `gbus564_coursework`:

- `gbus564_coursework.utils.course_data` — loaders for the course datasets
  (`load_churn()`, `load_housing()`, `load_online_retail()`,
  `load_aus_retail()`), which ship inside the package under
  `gbus564_coursework/data/`
- `gbus564_coursework.utils.sandbox` — synthetic-data generators used in the
  concept-demo notebooks
- `gbus564_coursework.utils.assignment_checks` — self-check helpers behind the
  assignment checkpoint cells

## Slides, syllabus, and course logistics

Posted on Canvas.
