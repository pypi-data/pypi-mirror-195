""" Sensospot Data Parser

Parsing the csv result files from Sensovations Sensospot image analysis.
"""

import logging
import pathlib
from datetime import datetime
from typing import Optional, Union

import pandas
from defusedxml import ElementTree

from . import columns, parameters

logger = logging.getLogger("sensospot_parser")

PathLike = Union[str, pathlib.Path]

RESULT_TAG_TYPES = {
    "System.Int32": int,
    "System.UInt32": int,
    "System.Double": float,
    "System.Boolean": lambda x: x.lower() == "true",
}

DATETIME_XML_FORMAT = "%m/%d/%Y %I:%M:%S %p"


class ParserTarget:
    """Class to parse the event stream emitted by ElementTree.XMLParser

    The methods "start()", "data()", "end()" and "close()" are defined
    according to the requirements of the ElementTree.XMLParser
    """

    def __init__(self):
        """initialization of the object instance"""
        self.collected = []
        self._current = {}
        self._data_func = None

    def start(self, tag: str, attributes: dict[str:str]) -> None:
        """start of an xml tag

        The sensovation software uses sometimes the attributes of a tag to
        store relevant data and sometimes the data part of the xml tree.

        This methods extracts the data from the attributes or preparse the
        parsing of the data section

        Args:
            tag:        the name of the tag
            attributes: the attributes of the tag as a dict
        """
        if tag == "ScanJobResult":
            self._current[columns.ANALYSIS_NAME] = attributes["ID"]
        elif tag == "AssayResult":
            well = attributes["ID"]
            self._current[columns.WELL_NAME] = attributes["ID"]
            self._current[columns.WELL_ROW] = well[0]
            self._current[columns.WELL_COLUMN] = int(well[1:])
        elif tag.startswith("ChannelConfig"):
            self._current[columns.EXPOSURE_ID] = int(tag[13:])
        elif tag == "Spot":
            self._current[columns.POS_ID] = int(attributes["ID"])
        elif tag == "Result":
            self._result_attributes_parser(attributes)
        elif tag == "Timestamp":
            self._data_func = self._data_timestamp_parser
        elif tag == "ImageFileName":
            self._data_func = self._data_image_name_parser

    def _result_attributes_parser(self, data: dict[str:str]) -> None:
        """parses the attributes of the "Result" tag"""
        label = data["Label"]
        converter = RESULT_TAG_TYPES.get(data["Type"], str)
        self._current[label] = converter(data["Value"])

    def _data_timestamp_parser(self, data: str) -> None:
        """parses the data section of a "Timestamp" tag"""
        timestamp = datetime.strptime(  # noqa: DTZ007
            data.strip(), DATETIME_XML_FORMAT
        )
        self._current[columns.ANALYSIS_DATETIME] = timestamp

    def _data_image_name_parser(self, data: str) -> None:
        """parses the data section of a "ImageFileName" tag"""
        self._current[columns.ANALYSIS_IMAGE] = data.strip()

    def data(self, data: str) -> None:
        """parses the data section of the xml tree

        The data sections in the xml tree of the sensovation software are
        not often used.

        The "start()" method sets a parser for the upcoming data section and
        this parser is removed after it was called.
        """
        if self._data_func:
            self._data_func(data)
            self._data_func = None

    def end(self, tag: str) -> None:
        """the end of a tag is reached

        If it is the end of a "Spot" tag, a copy of the current data is added
        to the collected data property.
        """
        if tag == "Spot":
            spot_data = dict(self._current)
            self.collected.append(spot_data)

    def closed(self) -> None:
        """the end of the xml file is reached"""


def _find_result_xml_file(folder: PathLike) -> Optional[pathlib.Path]:
    """searches a results folder for the analysis xml file

    There may be multiple xml files in the folder, but only one xsl file with
    the same (base) name as the xml file we are looking for. This is why we
    first look for the xsl file and then derive the path from the xml file
    from it.

    Args:
        folder:  path of folder containing data files

    Returns:
        Path to xml assay result file or None if it could not be found
    """
    source = pathlib.Path(folder)
    files = (i for i in source.iterdir() if i.is_file())
    not_hidden = (f for f in files if not f.name.startswith("."))
    xsl_files = [f for f in not_hidden if f.suffix == ".xsl"]
    if len(xsl_files) != 1:
        # multiple xsl files in a folder
        # this does not to be a "normal" results folder
        return None
    xsl_file = xsl_files[0]
    xml_file = xsl_file.with_suffix(".xml")
    return xml_file if xml_file.is_file() else None


def parse_xml_file(xml_file: PathLike) -> pandas.DataFrame:
    """parses an assay result xml file into a pandas data frame

    Will raise a ValueError on a non-parsable xml file.

    Args:
        xml_file:   path to the xml file

    Returns:
        A pandas DataFrame with the parsed data

    Raises:
        ValueError if the xml file could not be parsed
    """
    logger.info(f"Parsing xml results file {xml_file}")
    xml_file = pathlib.Path(xml_file)
    if not xml_file.is_file():
        msg = "Xml file does not exist"
        logger.debug(f"{msg}: {xml_file}")
        raise ValueError(msg)

    target = ParserTarget()
    parser = ElementTree.DefusedXMLParser(target=target)

    try:
        parser.feed(xml_file.read_text())
    except (IndexError, KeyError, ValueError, TypeError) as e:
        msg = "Malformed data in xml file"
        logger.warning(f"{msg} {xml_file}")
        raise ValueError(msg) from e

    data_frame = pandas.DataFrame(data=target.collected).reset_index()
    if data_frame.empty:
        msg = "Could not parse assay results xml file"
        logger.warning(f"{msg} {xml_file}")
        raise ValueError(msg)

    return columns._cleanup_data_columns(data_frame)


def parse_xml_folder(folder: PathLike) -> pandas.DataFrame:
    """parses the xml result file in a folder to one large dataframe

    Will raise an ValueError, if no sensospot data could be found in
    the folder

    Args:
        folder:  path of folder containing data files

    Returns:
        a pandas data frame with parsed data
    """
    folder = pathlib.Path(folder)
    xml_file = _find_result_xml_file(folder)
    if xml_file is None:
        msg = "Could not find assay results xml file"
        logger.debug(f"{msg} in folder {folder}")
        raise ValueError(msg)
    data_frame = parse_xml_file(xml_file)
    data_frame = parameters.add_measurement_parameters(data_frame, folder)
    return columns._cleanup_data_columns(data_frame)
