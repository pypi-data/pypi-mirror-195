""" Sensospot Data Parser

Parsing the csv result files from Sensovations Sensospot image analysis.
"""

import logging
import pathlib
import re
from collections import namedtuple
from typing import Optional, Sequence, TextIO, Union

import pandas

from . import columns
from .parameters import add_measurement_parameters

logger = logging.getLogger("sensospot_parser")

PathLike = Union[str, pathlib.Path]

REGEX_WELL = re.compile(
    r"""
    (?P<row>([A-Z]+))  # row name containing one or more letters
    (?P<column>(\d+))     # column, one or more decimals
    """,
    re.VERBOSE | re.IGNORECASE,
)

FileInfo = namedtuple("FileInfo", ["row", "column", "exposure"])


def _guess_decimal_separator(file_handle: TextIO) -> str:
    """guesses the decimal spearator of a opened data file

    This is a very crude method, but depending on the language setting,
    different decimal separators may be used.

    Args:
        file_handle:  a file handle to an opened csv file

    Returns:
        either '.' or ',' as a decimal separator
    """
    file_handle.seek(0)
    headers = next(file_handle)  # noqa: F841
    data = next(file_handle)
    separator = "," if data.count(",") > data.count(".") else "."
    file_handle.seek(0)
    return separator


def _parse_csv(data_file: PathLike) -> pandas.DataFrame:
    """parse a csv sensovation data file

    Tries to guess the decimal separator from the file contents

    Args:
        data_file: path to the csv file

    Returns:
        pandas data frame with the parsed data
    """
    data_path = pathlib.Path(data_file)
    with data_path.open("r") as handle:
        decimal_sep = _guess_decimal_separator(handle)
        handle.seek(0)
        return pandas.read_csv(handle, sep="\t", decimal=decimal_sep)


def _extract_measurement_info(data_file: PathLike) -> FileInfo:
    """extract measurement meta data from a file name

    Args:
        data_file:  path to the csv data file

    Returns:
        named tuple FileInfo with parsed metadata
    """
    data_path = pathlib.Path(data_file)
    *rest, well, exposure = data_path.stem.rsplit("_", 2)
    matched = REGEX_WELL.match(well)
    if matched is None:
        msg = f"not a valid well: '{well}'"
        raise ValueError(msg)
    row = matched["row"].upper()
    column = int(matched["column"])
    exposure = int(exposure)
    return FileInfo(row, column, exposure)


def parse_csv_file(data_file: PathLike) -> pandas.DataFrame:
    """parses one data file and adds metadata to result

    will race a ValueError, if metadata could not be extracted

    Args:
        data_file: path to the csv data file

    Returns:
        pandas data frame with the parsed data

    Raises:
        ValueError: if metadata could not be extracted
    """
    data_path = pathlib.Path(data_file).resolve()
    logger.debug(f"Parsing csv file {data_path}")
    measurement_info = _extract_measurement_info(data_path)
    data_frame = _parse_csv(data_path)
    # normalized well name
    data_frame[
        columns.WELL_NAME
    ] = f"{measurement_info.row}{measurement_info.column:02d}"
    data_frame[columns.WELL_ROW] = measurement_info.row
    data_frame[columns.WELL_COLUMN] = measurement_info.column
    data_frame[columns.EXPOSURE_ID] = measurement_info.exposure
    data_frame[columns.ANALYSIS_NAME] = data_path.parent.name
    data_frame[columns.ANALYSIS_IMAGE] = data_path.with_suffix(".tif").name
    return columns._cleanup_data_columns(data_frame)


def _parse_csv_file_silenced(
    data_file: PathLike,
) -> Optional[pandas.DataFrame]:
    """parses one data file and adds metadata

    Safety checks are supressed

    Args:
        data_file: path to the csv data file

    Returns:
        pandas data frame with the parsed data or None on error
    """
    try:
        return parse_csv_file(data_file)
    except ValueError:
        return None


def parse_multiple_csv_files(
    file_list: Sequence[PathLike],
) -> pandas.DataFrame:
    """parses a list of file paths to one combined data frame

    Args:
        file_list: collection of paths to csv data files
    Returns:
        pandas data frame with all parsed data combined
    """
    if not file_list:
        msg = "Empty file list provided"
        raise ValueError(msg)
    collection = (_parse_csv_file_silenced(path) for path in file_list)
    filtered = (frame for frame in collection if frame is not None)
    data_frame = pandas.concat(filtered, ignore_index=True).reset_index()
    data_frame[columns.WELL_ROW] = data_frame[columns.WELL_ROW].astype(
        "category"
    )
    return data_frame


def find_csv_files(folder: PathLike) -> Sequence[pathlib.Path]:
    """returns all csv files in a folder

    Args:
        folder:  path to the folder to search for csv files

    Returns:
        iterator with the found csv files
    """
    folder_path = pathlib.Path(folder)
    files = (item for item in folder_path.iterdir() if item.is_file())
    visible = (item for item in files if not item.stem.startswith("."))
    return (item for item in visible if item.suffix.lower() == ".csv")


def _sanity_check(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    """checks some basic constrains of a combined data frame

    Args:
        data_frame: measurement data

    Returns:
        a pandas DataFrame

    Raises:
        ValueError: if basic constrains are not met
    """
    field_rows = len(data_frame[columns.WELL_ROW].unique())
    field_cols = len(data_frame[columns.WELL_COLUMN].unique())
    exposures = len(data_frame[columns.EXPOSURE_ID].unique())
    spot_positions = len(data_frame[columns.POS_ID].unique())
    expected_rows = field_rows * field_cols * exposures * spot_positions
    if expected_rows != len(data_frame):
        msg = f"Measurements are missing: {expected_rows} != {len(data_frame)}"
        raise ValueError(msg)
    # set the right data type for measurement columns
    for raw_column in columns.NUMERIC_COLUMNS:
        data_frame[raw_column] = pandas.to_numeric(data_frame[raw_column])
    return data_frame


def parse_csv_folder(
    folder: PathLike, *, quiet: bool = False
) -> pandas.DataFrame:
    """parses all csv files in a folder to one large dataframe

    Will raise an ValueError, if no sensospot data could be found in
    the folder

    Args:
        folder:  path of folder containing data files
        quiet:   skip sanity check, defaults to False

    Returns:
        a pandas data frame with parsed data
    """
    logger.info(f"Parsing csv files in folder {folder}")
    folder_path = pathlib.Path(folder)
    file_list = find_csv_files(folder_path)
    try:
        data_frame = parse_multiple_csv_files(file_list)
    except ValueError as e:
        msg = f"No sensospot data found in folder '{folder}'"
        logger.warning(msg)
        raise ValueError(msg) from e

    data_frame = add_measurement_parameters(data_frame, folder_path)

    # The csv parser is only used if the xml analysis file is not present
    # the xml file would hold the Analysis.Datetime value
    data_frame[columns.ANALYSIS_DATETIME] = None

    data_frame = columns._cleanup_data_columns(data_frame)

    if quiet:
        return data_frame
    return _sanity_check(data_frame)
