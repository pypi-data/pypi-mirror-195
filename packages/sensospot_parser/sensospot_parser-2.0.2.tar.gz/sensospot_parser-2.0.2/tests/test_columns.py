def test_cleanup_data_columns():
    from pandas import DataFrame
    from sensospot_parser.columns import _cleanup_data_columns

    columns = ["Rect.", "Contour", " ID ", "Found", "Dia."]
    data = {col: [i] for i, col in enumerate(columns)}
    data_frame = DataFrame(data=data)

    result = _cleanup_data_columns(data_frame)

    assert set(result.columns) == {"Pos.Id", "Spot.Found", "Spot.Diameter"}
    assert result["Pos.Id"][0] == 2
    assert result["Spot.Found"][0] == 3
    assert result["Spot.Diameter"][0] == 4
