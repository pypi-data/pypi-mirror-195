from pathlib import Path

import click

from energyplus_diffs.plot_vars import plot


@click.command(name="energyplus-diff-analysis")
@click.argument("baseline-csv", type=click.Path(exists=True))
@click.argument("modified-csv", type=click.Path(exists=True))
@click.argument("output-dir", type=click.Path(exists=True))
@click.option(
    "-p",
    "--plot-all-series",
    is_flag=True,
    required=False,
    default=False,
    help="Plot all series including series without diffs"
)
@click.option(
    "-a",
    "--create-archive",
    is_flag=True,
    required=False,
    default=False,
    help="Create archive of plots afterwards"
)
def cli(baseline_csv, modified_csv, output_dir, plot_all_series, create_archive):
    click.echo(f"Baseline CSV: {click.format_filename(baseline_csv)}")
    click.echo(f"Modified CSV: {click.format_filename(modified_csv)}")
    plot(
        base_path=Path(baseline_csv).resolve(),
        mod_path=Path(modified_csv).resolve(),
        out_dir=Path(output_dir).resolve(),
        plot_all_series=plot_all_series,
        create_archive=create_archive
    )
