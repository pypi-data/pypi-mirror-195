import datetime
import os
from math import ceil
from pathlib import Path
from textwrap import wrap
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd

from energyplus_diffs.compress import make_archive


class GenericError(Exception):
    pass


def plot(base_path: Union[str, Path],
         mod_path: Union[str, Path],
         out_dir: Union[str, Path] = None,
         plot_all_series: bool = False,
         create_archive: bool = False,
         cols: Union[str, list] = None,
         low_row_num: int = None,
         high_row_num: int = None,
         ):
    """
    Plots csv diffs

    :param base_path: path to baseline file
    :param mod_path: path to modified file
    :param out_dir: path to directory for plots to be saved
    :param plot_all_series: optional, default FALSE. plot all series including series without diffs
    :param create_archive: optional, default FALSE. create archive of plots afterwards
    :param cols: optional. string column name, or list of string column names to plot
    :param low_row_num: optional. lowest row number to be plotted, excluding header row
    :param high_row_num: optional. highest row number to be plotted, excluding header row
    :return:
    """

    # proper path objects
    base_path = Path(base_path)
    mod_path = Path(mod_path)

    # load data
    df_base = pd.read_csv(base_path)
    df_mod = pd.read_csv(mod_path)

    # make sure the number of rows match for each file
    if df_base.shape[0] != df_mod.shape[0]:
        msg = "Files do not have the same number of rows. Each file must contain the same number of rows.\n" \
              f"File: {base_path.name}, num rows: {df_base.shape[0]}\n" \
              f"File: {mod_path.name}, num rows: {df_mod.shape[0]}"
        raise GenericError(msg)

    # process available columns
    df_base.rename(columns=lambda x: x.strip(), inplace=True)
    df_mod.rename(columns=lambda x: x.strip(), inplace=True)
    base_cols = df_base.columns.tolist()
    mod_cols = df_mod.columns.tolist()

    # get rid of the index col
    if "Date/Time" in base_cols:
        base_cols.remove("Date/Time")
    if "Date/Time" in mod_cols:
        mod_cols.remove("Date/Time")

    # make sure we're only plotting columns that exist and that we want
    if cols is None:
        # only plot the columns contained in both files
        cols = list(set(base_cols) & set(mod_cols))
    else:
        # we"re only plotting a select number of columns
        if type(cols) is str:
            # for when cols takes a single string input
            cols = [cols]
        elif type(cols) is list:
            # for when cols takes a list input
            cols = [x.strip() for x in cols]

        # make sure both files have the requested columns
        if not all([x in base_cols for x in cols]):
            msg = f"File: {base_path.name} does not contain all requested columns"
            GenericError(msg)
        if not all([x in mod_cols for x in cols]):
            msg = f"File: {mod_path.name} does not contain all requested columns"
            GenericError(msg)

    # set low plot range based on row number
    if low_row_num is None:
        min_idx = 0
    else:
        min_idx = low_row_num - 1

    # set high plot range based on row number
    if high_row_num is None:
        max_idx = df_base.shape[0]
    else:
        max_idx = high_row_num - 1

    # setup plots folder
    parent_dir = Path(__file__).parent.parent
    if out_dir is None:
        plot_dir_path = parent_dir / "plots"
    else:
        plot_dir_path = Path(out_dir) / f"plots-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # create the plots dir if it doesn't exist
    if not plot_dir_path.exists():
        os.mkdir(plot_dir_path)

    # make plots
    for idx, c in enumerate(cols):
        try:
            # process the column to be plotted
            idx = [*range(min_idx + 1, max_idx + 1, 1)]
            base = df_base[c].iloc[min_idx:max_idx]
            base = base.reindex(idx)
            base = base.dropna()
            mod = df_mod[c].iloc[min_idx: max_idx]
            mod = mod.reindex(idx)
            mod = mod.dropna()
            diff = base - mod

            if not any([abs(x) > 0 for x in diff]) and not plot_all_series:
                print(f"Skipping: {c} - no diffs")
                continue
            elif all(x == 0 for x in [base.shape[0], mod.shape[0], diff.shape[0]]):
                print(f"Skipping: {c} - no data to plot")
                continue
            else:
                print(f"Plotting: {c}")

            # upper limit of 30 markers for the plot
            marker_interval = max(ceil(base.shape[0] / 30), 1)

            # create the figure and plot the series
            fig, ax1 = plt.subplots(1)
            lines = []
            if base.shape[0] > 0:
                lines.append(ax1.plot(base, marker="s", markevery=marker_interval)[0])
            if mod.shape[0] > 0:
                lines.append(ax1.plot(mod, marker="^", linestyle="--", markevery=marker_interval)[0])

            if diff.shape[0] > 0:
                ax2 = ax1.twinx()
                lines.append(ax2.plot(diff, marker=".", linestyle="-.", c="r", markevery=marker_interval)[0])
                # add a note for when we're not adding markers to all data points
                if marker_interval > 1:
                    ax2.annotate(f"Note: marker icons only shown every {marker_interval} points\n"
                                 f"for clarity",
                                 xy=(10, 10),
                                 xycoords="figure pixels",
                                 fontsize=8)
                ax2.set_ylabel("Delta (baseline - modified)")

            # primary x/y axis grid lines
            ax1.grid()

            # make a legend that contains all series
            line_labels = ["baseline", "modified", "delta"]
            fig.legend(lines, line_labels, loc="lower right", ncol=3)

            # final housekeeping
            plt.suptitle("\n".join(wrap(c)))
            fig_name = c.replace(" ", "_").replace("/", "-").replace(":", "_")
            fig_path = plot_dir_path / f"{fig_name}.png"
            plt.savefig(fig_path, bbox_inches="tight")
        except:  # noqa: E722
            print(f"Failed on: {c}")

    if create_archive:
        archive_path = str(plot_dir_path.parent.resolve() / f"{plot_dir_path.name}.zip")
        make_archive(str(plot_dir_path), archive_path)
        print(f"\nFiles saved to: {archive_path}")
    else:
        print(f"\nFiles saved to: {str(plot_dir_path.resolve())}")
