""" Sensospot Data Parser

Parsing the numerical output from Sensovations Sensospot image analysis.
"""

__version__ = "2.0.2"

import logging
import pathlib
from typing import Union

import click
import pandas

from . import columns  # noqa: F401
from .csv_parser import parse_csv_folder
from .xml_parser import parse_xml_folder

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sensospot_parser")

DEFAULT_OUTPUT_FILENAME = "collected_data.csv"

PathLike = Union[str, pathlib.Path]


def parse_folder(source: PathLike, *, quiet: bool = False) -> pandas.DataFrame:
    """parses an assay result folder

    The function will first try to use an assay results xml file, and will
    fall back to parsing csv files if the xml file could not be parsed.

    Args:
        folder:  path of folder containing the assay result
        quiet:   skip sanity check for csv files, defaults to False

    Returns:
        a pandas data frame with parsed data
    """
    try:
        return parse_xml_folder(source)
    except ValueError:
        pass
    logger.info(
        "Could not parse xml results file, using fall-back csv parsing"
    )
    return parse_csv_folder(source, quiet=quiet)


@click.command()
@click.argument(
    "sources",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    required=True,
    nargs=-1,
)
@click.option(
    "-o",
    "--output",
    is_flag=False,
    flag_value=DEFAULT_OUTPUT_FILENAME,
    type=click.Path(exists=False, dir_okay=False),
    help=f"Output file path, defaults to '{DEFAULT_OUTPUT_FILENAME}'",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Ignore sanity check for csv file parsing",
)
@click.option(
    "-v",
    "--verbose",
    help="Set verbosity of log, add multiple -vv for more verbose logging",
    count=True,
)
def main(sources, output, verbose, quiet=False):  # noqa: FBT002
    """Parses the measurement results of the Sensospot reader

    The resulting output is either echoed to stdout or saved to a file.

    At first parsing the assay result xml file is tried.
    If this doesn't work, the fallback is to parse the csv files.
    """

    if verbose == 0:
        logging.disable()
    elif verbose == 1:
        logging.disable(level=logging.DEBUG)
    else:
        logging.disable(level=logging.NOTSET)

    paths = (pathlib.Path(source) for source in sources)
    collection = (parse_folder(source, quiet=quiet) for source in paths)
    result = (
        pandas.concat(collection, ignore_index=True)
        .reset_index()
        .to_csv(output, sep="\t", index=False)
    )
    # if 'output' is None, the call to 'to_csv()' returns the csv as text
    # if 'output' is not None, 'to_csv()' writes to the file and returns None
    if result:
        click.echo(result)
