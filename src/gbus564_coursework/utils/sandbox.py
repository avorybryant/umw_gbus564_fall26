"""The synthetic-data sandbox: one reusable, parameterized generator per data
shape, dialed with noise / imbalance / confounding / drift to break a model
assumption on purpose. See
coursework/notebooks/week1/lectures/09_synthetic_data_sandbox.ipynb and
course_prep/schedule_overview.md for how each knob maps to a later lesson's
demo.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 564


def _rng(rng):
    return rng if rng is not None else np.random.default_rng(RANDOM_SEED)


def make_regression_sandbox(n_samples=200, n_features=1, noise=1.0, confound=False, rng=None):
    """Regression data. n_features=1 -> a true nonlinear (cubic) signal on
    one feature, for the W2 polynomial-overfitting demo. n_features>1 with
    confound=True -> features are pairwise correlated (rho=0.95), for the W3
    multicollinearity demo (coefficients become unstable / flip sign).
    Small n_samples with large n_features (confound=False) gives the W6
    over-parameterized case: mostly irrelevant features for the model to
    chase as noise.
    """
    rng = _rng(rng)

    if n_features == 1:
        x = rng.uniform(-3, 3, size=n_samples)
        y = 0.5 * x**3 - 2 * x + noise * rng.normal(size=n_samples)
        X = pd.DataFrame({"x": x})
        return X, pd.Series(y, name="y")

    rho = 0.95 if confound else 0.0
    cov = np.full((n_features, n_features), rho)
    np.fill_diagonal(cov, 1.0)
    X = rng.multivariate_normal(mean=np.zeros(n_features), cov=cov, size=n_samples)

    n_informative = min(3, n_features)
    beta = np.zeros(n_features)
    beta[:n_informative] = rng.uniform(1, 3, size=n_informative)
    y = X @ beta + noise * rng.normal(size=n_samples)

    X = pd.DataFrame(X, columns=[f"x{i}" for i in range(n_features)])
    return X, pd.Series(y, name="y")


def make_residual_diagnostics_sandbox(n_samples=150, regime="clean", noise=1.0, rng=None):
    """A single-feature linear truth (y = 2 + 3x) under three regimes, for
    the W3 residual-diagnostics insert: calibrate what a "clean" residual
    plot looks like before reading one on real (Ames) data.
    regime="clean" -> constant-variance noise (the textbook target).
    regime="heteroscedastic" -> noise scales with |x|, producing the classic
    fan shape when residuals are plotted against fitted values.
    regime="curved" -> the true relationship has an omitted quadratic term;
    fitting a straight line leaves a U-shaped residual pattern.
    """
    rng = _rng(rng)
    x = rng.uniform(-3, 3, size=n_samples)
    y = 2 + 3 * x

    if regime == "clean":
        y = y + noise * rng.normal(size=n_samples)
    elif regime == "heteroscedastic":
        y = y + noise * (1 + np.abs(x)) * rng.normal(size=n_samples)
    elif regime == "curved":
        y = y + 1.5 * x**2 + noise * rng.normal(size=n_samples)
    else:
        raise ValueError(
            f"unknown regime: {regime!r} (expected 'clean', 'heteroscedastic', 'curved')"
        )

    X = pd.DataFrame({"x": x})
    return X, pd.Series(y, name="y")


def make_classification_sandbox(n_samples=300, n_features=1, noise=0.3, imbalance=0.5, rng=None):
    """Binary classification data. n_features=1 -> a single continuous score
    with class separation controlled by noise, for the W2 threshold/stump
    demo (slide the cutoff, watch ROC/PR trace out). imbalance is the
    positive-class proportion, feeding the accuracy-paradox discussion.
    n_features>1 delegates to sklearn's make_classification for the general
    case.
    """
    rng = _rng(rng)
    n_pos = int(round(n_samples * imbalance))
    n_neg = n_samples - n_pos
    y = np.concatenate([np.zeros(n_neg), np.ones(n_pos)]).astype(int)

    if n_features == 1:
        separation = 2.0
        score = np.where(y == 1, separation, 0.0) + noise * rng.normal(size=n_samples)
        order = rng.permutation(n_samples)
        X = pd.DataFrame({"score": score[order]})
        y = pd.Series(y[order], name="y")
        return X, y

    from sklearn.datasets import make_classification

    seed = int(rng.integers(0, 2**31 - 1))
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=min(3, n_features),
        weights=[1 - imbalance, imbalance],
        flip_y=min(noise, 0.5),
        random_state=seed,
    )
    X = pd.DataFrame(X, columns=[f"x{i}" for i in range(n_features)])
    return X, pd.Series(y, name="y")


def make_clusters_sandbox(n_samples=300, shape="blobs", noise=1.0, rng=None):
    """Unlabeled 2D data for clustering. shape="blobs" is k-means-friendly
    (spherical, well-separated); shape="moons" or "anisotropic" breaks
    k-means's spherical-cluster assumption on purpose (W4). Returns (X,
    true_labels) — labels are for comparing against, never fed to k-means.
    """
    rng = _rng(rng)
    seed = int(rng.integers(0, 2**31 - 1))

    if shape == "blobs":
        from sklearn.datasets import make_blobs

        X, labels = make_blobs(
            n_samples=n_samples, centers=3, cluster_std=noise, random_state=seed
        )
    elif shape == "moons":
        from sklearn.datasets import make_moons

        X, labels = make_moons(n_samples=n_samples, noise=noise * 0.1, random_state=seed)
    elif shape == "anisotropic":
        from sklearn.datasets import make_blobs

        # Fixed layout (not derived from rng): this specific center/shear
        # combination is what makes k-means visibly misassign points along
        # the elongation — an arbitrary blob layout mostly doesn't. Noise
        # still scales cluster_std, so the break gets more/less pronounced.
        X, labels = make_blobs(n_samples=n_samples, cluster_std=noise, random_state=170)
        transform = np.array([[0.60834549, -0.63667341], [-0.40887718, 0.85253229]])
        X = X @ transform
    else:
        raise ValueError(f"unknown shape: {shape!r} (expected 'blobs', 'moons', 'anisotropic')")

    X = pd.DataFrame(X, columns=["x0", "x1"])
    return X, pd.Series(labels, name="cluster")


def make_timeseries_sandbox(
    n_periods=365, trend=0.0, seasonality=1.0, noise=1.0, drift=0.0, rng=None
):
    """A daily time series with weekly seasonality, for the W7 leakage demo
    (shuffle it and a random split leaks the future via autocorrelation) and
    the drift/monitoring thread (W1 Lesson 5). drift shifts the series' level
    partway through — a regime change, the kind that should trip a monitor.
    """
    rng = _rng(rng)
    t = np.arange(n_periods)
    seasonal = seasonality * np.sin(2 * np.pi * t / 7)
    level_shift = np.where(t >= n_periods * 0.7, drift, 0.0)
    y = 10 + trend * t + seasonal + level_shift + noise * rng.normal(size=n_periods)

    dates = pd.date_range("2024-01-01", periods=n_periods, freq="D")
    return pd.Series(y, index=dates, name="y")
