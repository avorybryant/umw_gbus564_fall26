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

This repo is managed with [`uv`](https://docs.astral.sh/uv/) (Python 3.12+):

```
uv sync
uv run jupyter lab
```

`uv sync` installs the helper package plus everything the notebooks import
(TensorFlow/Keras, XGBoost, SHAP, statsmodels, …).

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
