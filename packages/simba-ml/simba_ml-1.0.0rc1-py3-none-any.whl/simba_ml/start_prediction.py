"""Module for starting a prediction pipeline."""
import typing
import argparse
import logging
import datetime

import pandas as pd

from simba_ml.prediction.time_series.pipelines import synthetic_data_pipeline

logger = logging.getLogger(__name__)


class Pipeline(typing.Protocol):
    """Protocol for a prediction pipeline."""

    def __call__(self, config_path: str) -> pd.DataFrame:
        """Runs the Pipeline.

        Args:
            config_path: path to the config file.
        """


PIPELINES: typing.Dict[str, Pipeline] = {
    "synthetic_data": synthetic_data_pipeline.main,
}


def start_prediction(pipeline, output_path, config_path) -> None:
    """Start a prediction pipeline."""
    results = PIPELINES[args.pipeline](args.config_path)
    results.to_csv(args.output_path)
