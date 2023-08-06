from datetime import datetime

import pytest

from .conftest import EXAMPLE_DIR_XML_WITH_PARAMS, EXAMPLE_DIR_XML_WO_PARAMS


class DummyDataFunc:
    def __init__(self, as_bool):
        self.data = None
        self.as_bool = as_bool

    def __call__(self, data):
        self.data = data

    def __bool__(self):
        return self.as_bool


def test_parser_target_init():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()

    assert target.collected == []
    assert target._current == {}
    assert target._data_func is None


@pytest.mark.parametrize(
    ("tag", "attributes", "expected"),
    [
        ("UnknownTag", {"ID": "something"}, {}),
        (
            "ScanJobResult",
            {"ID": "scan job 1"},
            {"Analysis.Name": "scan job 1"},
        ),
        (
            "AssayResult",
            {"ID": "C03"},
            {"Well.Name": "C03", "Well.Row": "C", "Well.Column": 3},
        ),
        ("ChannelConfig1", {}, {"Exposure.Id": 1}),
        ("Spot", {"ID": "456"}, {"Pos.Id": 456}),
        (
            "Result",
            {"Label": "a label", "Type": "Unknown", "Value": "a value"},
            {"a label": "a value"},
        ),
    ],
)
@pytest.mark.parametrize("additionals", [{}, {"Ignored": "value"}])
def test_parser_target_start_simple_attributes(
    tag, attributes, additionals, expected
):
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    attributes.update(additionals)

    target.start(tag, attributes)  # stateful operation

    assert target._current == expected
    assert target._data_func is None


def test_parser_target_start_timestamp():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    target.start("Timestamp", {})

    assert target._data_func == target._data_timestamp_parser


def test_parser_target_start_image_file_name():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    target.start("ImageFileName", {})

    assert target._data_func == target._data_image_name_parser


@pytest.mark.parametrize(
    ("data_type", "value", "expected"),
    [
        ("unknown type", 1, "1"),
        ("System.Int32", "12", 12),
        ("System.UInt32", "23", 23),
        ("System.Double", "4.56", 4.56),
        ("System.Boolean", "true", True),
        ("System.Boolean", "True", True),
        ("System.Boolean", "Xrue", False),
    ],
)
def test_parser_target_result_attributes_parser(data_type, value, expected):
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    data = {"Label": "some label", "Type": data_type, "Value": value}

    target._result_attributes_parser(data)  # stateful operation

    assert target._current == {"some label": expected}
    assert type(target._current["some label"]) == type(expected)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            "3/7/2022 5:31:47 PM",
            datetime(2022, 3, 7, 17, 31, 47),  # noqa: DTZ001
        ),
        (
            "03/7/2022 5:31:47 PM",
            datetime(2022, 3, 7, 17, 31, 47),  # noqa: DTZ001
        ),
        (
            "3/07/2022 5:31:47 PM",
            datetime(2022, 3, 7, 17, 31, 47),  # noqa: DTZ001
        ),
        (
            "03/07/2022 5:31:47 PM",
            datetime(2022, 3, 7, 17, 31, 47),  # noqa: DTZ001
        ),
        (
            "3/7/2022 5:3:47 PM",
            datetime(2022, 3, 7, 17, 3, 47),  # noqa: DTZ001
        ),
        (
            "3/7/2022 5:31:4 PM",
            datetime(2022, 3, 7, 17, 31, 4),  # noqa: DTZ001
        ),
        (
            "3/7/2022 5:31:47 pm",
            datetime(2022, 3, 7, 17, 31, 47),  # noqa: DTZ001
        ),
        (
            "3/7/2022 5:31:47 AM",
            datetime(2022, 3, 7, 5, 31, 47),  # noqa: DTZ001
        ),
    ],
)
def test_parser_target_data_timestamp_parser(value, expected):
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()

    target._data_timestamp_parser(value)  # stateful operation

    assert target._current == {"Analysis.Datetime": expected}


def test_parser_target_data_image_name_parser():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()

    target._data_image_name_parser(" some file path ")  # stateful operation

    assert target._current == {"Analysis.Image": "some file path"}


def test_parser_target_data_does_not_call_function():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    dummy = DummyDataFunc(as_bool=False)
    target._data_func = dummy

    target.data("some data")  # the NotImplementedError is not raised

    assert dummy.data is None


def test_parser_target_data_does_call_function():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    dummy = DummyDataFunc(as_bool=True)
    target._data_func = dummy

    target.data("some data")  # stateful operation

    assert dummy.data == "some data"


def test_parser_target_data_reacts_on_spot():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    target._current = {"some current": "data values"}

    target.end("Spot")  # stateful operation

    assert target.collected == [{"some current": "data values"}]
    assert target.collected[0] is not target._current


def test_parser_target_data_does_only_react_on_spot():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()
    target._current = {"some current": "data values"}

    target.end("NonSpotTag")  # stateful operation

    assert target.collected == []


def test_parser_target_closed():
    from sensospot_parser.xml_parser import ParserTarget

    target = ParserTarget()

    target.closed()  # stateful operation, must be callable


def test_find_result_xml_file_ok(tmp_path):
    from sensospot_parser.xml_parser import _find_result_xml_file

    xls_file = tmp_path / "result.xsl"
    xls_file.touch()
    xml_file = tmp_path / "result.xml"
    xml_file.touch()

    result = _find_result_xml_file(tmp_path)

    assert result == xml_file


def test_find_result_xml_file_no_matching_xml_file(tmp_path):
    from sensospot_parser.xml_parser import _find_result_xml_file

    xls_file = tmp_path / "result.xsl"
    xls_file.touch()
    xml_file = tmp_path / "other.xml"
    xml_file.touch()

    result = _find_result_xml_file(tmp_path)

    assert result is None


def test_find_result_xml_file_no_xsl_file(tmp_path):
    from sensospot_parser.xml_parser import _find_result_xml_file

    xml_file = tmp_path / "result.xml"
    xml_file.touch()

    result = _find_result_xml_file(tmp_path)

    assert result is None


def test_find_result_xml_file_multiple_xsl_files(tmp_path):
    from sensospot_parser.xml_parser import _find_result_xml_file

    xls_file = tmp_path / "result.xsl"
    xls_file.touch()
    surplus_file = tmp_path / "surplus.xsl"
    surplus_file.touch()
    xml_file = tmp_path / "result.xml"
    xml_file.touch()

    result = _find_result_xml_file(tmp_path)

    assert result is None


def test_find_result_hidden_xsl_file(tmp_path):
    from sensospot_parser.xml_parser import _find_result_xml_file

    xls_file = tmp_path / ".result.xsl"
    xls_file.touch()
    xml_file = tmp_path / ".result.xml"
    xml_file.touch()

    result = _find_result_xml_file(tmp_path)

    assert result is None


def test_parse_xml_file_ok(example_dir):
    import pandas
    from sensospot_parser.xml_parser import (
        _find_result_xml_file,
        parse_xml_file,
    )

    folder = example_dir / EXAMPLE_DIR_XML_WO_PARAMS
    xml_file = _find_result_xml_file(folder)

    result = parse_xml_file(xml_file)

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 4 * 4 * 4 * 100
    assert set(result["Well.Row"]) == set("ABCD")
    assert set(result["Well.Column"]) == {1, 2, 3, 4}
    assert set(result["Exposure.Id"]) == {1, 2, 3, 4}
    assert min(result["Spot.Diameter"]) == 22
    assert max(result["Spot.Diameter"]) == 34
    assert "Parameters.Time" not in result


@pytest.mark.parametrize(
    ("file_name", "message"),
    [
        ("not_existing.xml", "Xml file does not exist"),
        ("defect.xml", "Could not parse assay results xml file"),
        ("malformed_data.xml", "Malformed data in xml file"),
    ],
)
def test_parse_xml_file_raies_error(file_name, message, example_dir):
    from sensospot_parser.xml_parser import parse_xml_file

    xml_file = example_dir / file_name

    with pytest.raises(ValueError) as e:  # noqa: PT011
        parse_xml_file(xml_file)

    assert message in str(e)


def test_parse_xml_folder_with_params(example_dir):
    import pandas
    from sensospot_parser.xml_parser import parse_xml_folder

    folder = example_dir / EXAMPLE_DIR_XML_WITH_PARAMS

    result = parse_xml_folder(folder)

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 4 * 4 * 4 * 100
    assert not result["Parameters.Time"].hasnans


def test_parse_xml_folder_without_params(example_dir):
    import pandas
    from sensospot_parser.xml_parser import parse_xml_folder

    folder = example_dir / EXAMPLE_DIR_XML_WO_PARAMS

    result = parse_xml_folder(folder)

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 4 * 4 * 4 * 100
    assert result["Parameters.Time"].hasnans


def test_parse_xml_folder_non_existing_xml_file(tmp_path):
    from sensospot_parser.xml_parser import parse_xml_folder

    with pytest.raises(ValueError) as e:  # noqa: PT011
        parse_xml_folder(tmp_path)

    assert "Could not find assay results xml file" in str(e)
