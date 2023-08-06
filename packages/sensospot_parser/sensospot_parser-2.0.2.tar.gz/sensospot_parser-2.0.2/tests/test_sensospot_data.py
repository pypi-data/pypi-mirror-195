""" testing the __ini__ file """
import pytest

from .conftest import EXAMPLE_DIR_CSV_WO_PARAMS, EXAMPLE_DIR_XML_WO_PARAMS


def test_import_api():
    from sensospot_parser import (
        columns,  # noqa: F401
        main,  # noqa: F401
        parse_csv_folder,  # noqa: F401
        parse_folder,  # noqa: F401
        parse_xml_folder,  # noqa: F401
    )


def test_compare_xml_to_csv(example_dir):
    import pandas
    from sensospot_parser import parse_csv_folder, parse_xml_folder

    folder = example_dir / EXAMPLE_DIR_XML_WO_PARAMS

    csv_df = parse_csv_folder(folder)
    xml_df = parse_xml_folder(folder)

    assert isinstance(csv_df, pandas.DataFrame)
    assert isinstance(xml_df, pandas.DataFrame)

    assert len(csv_df) == len(xml_df)
    assert set(csv_df.columns) == set(xml_df.columns)
    assert set(csv_df["Well.Name"]) == set(xml_df["Well.Name"])
    assert set(csv_df["Exposure.Id"]) == set(xml_df["Exposure.Id"])
    assert set(csv_df["Spot.Diameter"]) == set(xml_df["Spot.Diameter"])


@pytest.mark.parametrize(
    ("folder", "length", "hasnans"),
    [
        (EXAMPLE_DIR_XML_WO_PARAMS, 6400, False),
        (EXAMPLE_DIR_CSV_WO_PARAMS, 28800, True),
    ],
)
def test_parse_folder_switches_parser(example_dir, folder, length, hasnans):
    import pandas
    from sensospot_parser import parse_folder

    result = parse_folder(example_dir / folder)

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == length
    assert result["Analysis.Datetime"].hasnans == hasnans
