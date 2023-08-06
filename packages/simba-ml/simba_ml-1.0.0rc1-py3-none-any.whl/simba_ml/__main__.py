import importlib
import datatime

import click

from simba_ml.simulation import generators
from simba_ml import start_prediction


GENERATORS = {
    "TimeSeriesGenerator": generators.TimeSeriesGenerator,
    "TimePointsGenerator": generators.TimePointsGenerator,
    "SteadyStateGenerator": generators.SteadyStateGenerator,
}


@click.group()
def main():
    pass


@click.command()
@click.option(
    "--generator",
    default="TimeSeriesGenerator",
    type=click.Choice(GENERATORS.keys()),
    help="Which generator to use."
)
@click.option("--config-file", help="Config File containing an System Model called sm.")
@click.option("--n", default=100, help="Number of samples to generate.")
def generate_data(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    sm = importlib.import_module(__normalize_module_name(args.module)).sm
    GENERATORS[generator](sm).generate_csvs()


@click.command()
@click.argument(
    "pipeline",
    type=click.Choice(start_prediction.PIPELINES.keys()),
    help="The name of the pipeline to run.",
    required=True,
)
@click.option(
    "--output-path",
    type=str,
    default=f"results{datetime.datetime.now()}.csv",
    help="Path to the output file.",
)
@click.option(
    "--config-path",
    type=str,
    default="config.toml",
    help="Path to the config file.",
)
def start_prediction_command():
    """Start a prediction pipeline."""
    start_prediction.start_prediction(pipeline, output_path, config_path)


main.add_command(generate_data)
main.add_command(start_prediction_command)


if __name__ == "__main__":
    main()
