from cgi import FieldStorage
from typing import Tuple, List, Dict
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tonic_reporting.util import filter_null_and_match_row_counts
from scipy.stats import ks_2samp, anderson_ksamp, chisquare, mannwhitneyu
from scipy.special import kl_div

from tonic_reporting.styling import Colors, PlotsSizes, Labels, FontSizes


def summarize_numeric(
    real_data: pd.DataFrame, synth_data: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    rows = []
    for col in columns:
        real = real_data[col]
        fake = synth_data[col]
        anderson_stat, _, anderson_p_val = anderson_ksamp([real, fake])
        ks_stat, ks_p_val = ks_2samp(real, fake)
        mwu_stat, mwu_p_val = mannwhitneyu(real, fake)
        row = {
            "Column": col,
            "Anderson-Darling statistic": anderson_stat,
            "Anderson-Darling p-value": anderson_p_val,
            "Kolmogorov-Smirnov statistic": ks_stat,
            "Kolmogorov-Smirnov p-value": ks_p_val,
            "Mann-Whitney statistics": mwu_stat,
            "Mann-Whitney p-value": mwu_p_val,
        }

        rows.append(row)

    return pd.DataFrame(rows)


def get_frequencies(
    real_series: pd.Series, synthetic_series: pd.Series
) -> Tuple[np.ndarray, np.ndarray]:
    """Gets frequencies for each value in real and synthetic series. Assumes synthetic series values
    are subset of series_values
    """
    real_ft = real_series.value_counts()
    fake_ft = synthetic_series.value_counts()
    real_counts = []
    fake_counts = []
    for value in real_ft.keys():
        real_counts.append(real_ft[value])
        fake_counts.append(fake_ft.get(value, 0))
    return np.array(real_counts), np.array(fake_counts)


def compute_empirical_cdf(samples: np.ndarray, ci_val=0.95, sort=False):
    if not sort:
        sorted_samples = np.sort(samples)
    else:
        sorted_samples = samples
    x = sorted_samples
    n = len(x)
    y = np.cumsum(np.ones(x.shape)) / n
    alpha = 1 - ci_val
    if 1 > alpha > 0:
        eps = np.sqrt(np.log(2 / alpha) / (2 * n))
        lower = np.maximum(y - eps, 0)
        upper = np.minimum(y + eps, 1)
    else:
        lower = y
        upper = y
    return x, y, lower, upper


def compare_stepwise_curves(
    x_0: np.ndarray, y_0: np.ndarray, x_1: np.ndarray, y_1: np.ndarray, lower_bound=0
):
    """Compares the stepwise function f=(x_0, y_0) and g=(x_1, y_1) to determine if f>= g where f>=lower_bound"""
    idx = np.searchsorted(x_0, x_1, side="right")
    comparable = np.where(x_1 <= np.max(x_0))[0]
    return np.all(
        np.logical_or(
            y_0[idx[comparable]] <= lower_bound, y_1[comparable] <= y_0[idx[comparable]]
        )
    )


def chi_square_test(
    real_data: pd.Series, synthetic_data: pd.Series
) -> Tuple[float, float]:
    real_counts, fake_counts = get_frequencies(
        real_data,
        synthetic_data,
    )
    return chisquare(fake_counts, real_counts)


def kl_divergence(real_data: pd.Series, synthetic_data: pd.Series) -> float:
    """Computes D_KL(synthetic_data || real_data)"""
    real_counts, fake_counts = get_frequencies(
        real_data,
        synthetic_data,
    )
    idx = np.where(fake_counts != 0)[0]
    real_probs = real_counts[idx] / sum(real_counts[idx])
    fake_probs = fake_counts[idx] / sum(fake_counts[idx])

    return np.sum(fake_probs * np.log(fake_probs / real_probs))


def valid_chi_square_params(real: pd.Series, fake: pd.Series, col):
    """
    Check to see if chi_square test is valid.

    Based on first paragraph of the Notes section of the scipy docs
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
    """
    if len(real) != len(fake):
        warnings.warn(f"for {col} column chi squared test invalid so skipping")
    real_vcs = real.value_counts()
    fake_vcs = fake.value_counts()
    if set(real_vcs.index) != set(fake_vcs.index):
        warnings.warn(f"for {col} column chi squared test invalid so skipping")
        return False
    if real_vcs.iloc[-1] <= 5 or fake_vcs.iloc[-1] <= 5:
        warnings.warn(
            f"for {col} column chi squared test invalid so skipping", stacklevel=2
        )
        return False
    return True


def summarize_categorical(
    real_data: pd.DataFrame, synth_data: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    rows = []
    for col in columns:
        real = real_data[col]
        fake = synth_data[col]

        do_chi_square_test = valid_chi_square_params(real, fake, col)
        if do_chi_square_test:
            cs_stat, cs_p_val = chi_square_test(real, fake)
        else:
            cs_stat, cs_p_val = np.nan, np.nan
        kl = kl_divergence(real_data[col], synth_data[col])
        row = {
            "Column": col,
            "Chi-Square statistic": cs_stat,
            "Chi-Square p-value": cs_p_val,
            "D_KL(Synth || Real)": kl,
        }
        rows.append(row)
    return pd.DataFrame(rows)


def plot_all_marginals(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    numeric_columns: List[str],
    categorical_columns: List[str],
    figsize=None,
) -> None:
    n_plots = len(numeric_columns) + len(categorical_columns)
    n_rows = int((n_plots + n_plots % 2) // 2)
    if figsize is None:
        figsize = (2 * PlotsSizes.DEFAULT_WIDTH, n_rows * PlotsSizes.DEFAULT_HEIGHT)
    fig, axarr = plt.subplots(n_rows, 2, figsize=figsize, tight_layout=True)
    for col, ax in zip(numeric_columns, axarr.ravel()):
        plot_histogram(real_data, synth_data, col, ax=ax)
    for col, ax in zip(categorical_columns, axarr.ravel()[len(numeric_columns) :]):
        plot_frequency_table(real_data, synth_data, col, ax=ax)
    plt.show(block=False)


def plot_histogram(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    col: str,
    ax=None,
    side_by_side=False,
    lower_quantile_lim=0.005,
    upper_quantile_lim=0.995,
):
    real_data, synth_data = filter_null_and_match_row_counts(
        real_data, synth_data, [col]
    )

    if ax is None:
        fig, ax = plt.subplots(1, 1)
    bins = np.histogram_bin_edges(np.array(real_data[col]), bins="auto")
    if side_by_side:
        ax.hist(
            [real_data[col], synth_data[col]],
            bins=bins,
            color=[Colors.REAL, Colors.SYNTH],
            label=[Labels.REAL, Labels.SYNTH],
        )
    else:
        ax.hist(
            real_data[col],
            bins=bins,
            color=Colors.REAL,
            alpha=Colors.ALPHA,
            label=Labels.REAL,
        )
        ax.hist(
            synth_data[col],
            bins=bins,
            color=Colors.SYNTH,
            alpha=Colors.ALPHA,
            label=Labels.SYNTH,
        )
    ax.set_xlim(
        real_data[col].quantile(lower_quantile_lim),
        real_data[col].quantile(upper_quantile_lim),
    )
    ax.legend()
    ax.set_title(col)
    ax.tick_params(axis="both", which="major")


def plot_frequency_table(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    col: str,
    ax=None,
):
    vcs = pd.concat(
        [real_data[col].value_counts(), synth_data[col].value_counts()], axis=1
    )
    vcs.columns = ["Real", "Synthetic"]
    if vcs.shape[0] > 50:
        figsize = (2 * PlotsSizes.DEFAULT_WIDTH, PlotsSizes.DEFAULT_HEIGHT)
    else:
        figsize = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
    x_labels = list(vcs.index)
    x_axis = np.arange(len(x_labels))
    width = 0.2
    ax.bar(x_axis - width, vcs["Real"], 0.4, label="Real", color=Colors.REAL)
    ax.bar(x_axis + width, vcs["Synthetic"], 0.4, label="Synthetic", color=Colors.SYNTH)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(x_labels, rotation="vertical")
    ax.legend()
    ax.set_title(col)


def plot_sequence_lengths(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    groupby_col: str,
    ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    sequence_lengths = real_data.groupby(groupby_col).apply(len)
    bin_tuple = ax.hist(
        sequence_lengths,
        bins=max(sequence_lengths),
        color=Colors.REAL,
        alpha=Colors.ALPHA,
        label=Labels.REAL,
    )
    _ = ax.hist(
        synth_data.groupby(groupby_col).apply(len),
        bins=bin_tuple[1],
        color=Colors.SYNTH,
        alpha=Colors.ALPHA,
        label=Labels.SYNTH,
    )
    ax.legend()
    ax.set_title("Sequence Lengths")


def plot_event_counts(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    orderby_col: str,
    ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    bin_tuple = ax.hist(
        real_data[orderby_col],
        bins=real_data[orderby_col].nunique(),
        color=Colors.REAL,
        alpha=Colors.ALPHA,
        label=Labels.REAL,
    )
    _ = ax.hist(
        synth_data[orderby_col],
        bins=bin_tuple[1],
        color=Colors.SYNTH,
        alpha=Colors.ALPHA,
        label=Labels.REAL,
    )
    ax.set_title(f"Events per {orderby_col}")
    ax.legend()


# TODO: possibly deprecate these methods, or at least rewrite to be flexible
# with time and sequence lengths
def plot_events_means(
    real_data: pd.DataFrame, synth_data: pd.DataFrame, col: str, order_col: str, ax=None
):
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    real_agg = real_data.groupby(order_col)[col].agg("mean")
    synth_agg = synth_data.groupby(order_col)[col].agg("mean")
    # both will use x-axis given by the real data
    x_vals = list(real_agg.index)
    real_vals = list(real_agg)
    synth_vals = list(synth_agg)
    ax.plot(x_vals, real_vals, label=Labels.REAL, color=Colors.REAL)
    ax.plot(x_vals, synth_vals, label=Labels.SYNTH, color=Colors.SYNTH)
    ax.legend(fontsize=FontSizes.DEFAULT)
    ax.set_xlabel(order_col, fontsize=FontSizes.DEFAULT)
    ax.set_title(col + " Average", fontsize=FontSizes.DEFAULT)


def plot_events_confidence_intervals(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    col: str,
    order_col: str,
    lower_q=0.025,
    upper_q=0.975,
    ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    def lower(x):
        return x.quantile(q=lower_q)

    def upper(x):
        return x.quantile(q=upper_q)

    real_agg = real_data.groupby(order_col)[col].agg(["mean", lower, upper])
    synth_agg = synth_data.groupby(order_col)[col].agg(["mean", lower, upper])
    # both will use x-axis given by the real data
    x_vals = list(real_agg.index)
    ax.plot(
        x_vals, list(real_agg["mean"]), label=Labels.REAL + " Mean", color=Colors.REAL
    )
    ax.fill_between(
        x_vals,
        list(real_agg["lower"]),
        list(real_agg["upper"]),
        alpha=0.2,
        color=Colors.REAL,
        label=Labels.REAL + " Conf Int",
    )
    ax.plot(
        x_vals,
        list(synth_agg["mean"]),
        label=Labels.SYNTH + " Mean",
        color=Colors.SYNTH,
    )
    ax.fill_between(
        x_vals,
        list(synth_agg["lower"]),
        list(synth_agg["upper"]),
        alpha=0.2,
        color=Colors.SYNTH,
        label=Labels.SYNTH + " Conf Int",
    )
    ax.legend(fontsize=FontSizes.DEFAULT)
    conf_perc = str(round(100 * (upper_q - lower_q)))
    title = col + " " + conf_perc + "% Confidence Intervals"
    ax.set_xlabel(order_col, fontsize=FontSizes.DEFAULT)
    ax.set_title(title, fontsize=FontSizes.DEFAULT)
