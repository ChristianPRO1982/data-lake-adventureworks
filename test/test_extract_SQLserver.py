from unittest.mock import patch, MagicMock
import source.extract_SQLserver as extract_SQLserver



def test_init():
    result = extract_SQLserver.init()
    assert result == True

@patch("source.extract_SQLserver.connect")
@patch("os.getenv")
def test_connect(mock_getenv, mock_create_engine):
    mock_getenv.side_effect = lambda key: {
        "DRIVER": "ODBC Driver 18 for SQL Server",
        "SERVER": "localhost",
        "DATABASE": "TestDB",
        "UID": "test_user",
        "PWD": "test_password",
        "ENCRYPT": "no",
        "TRUSTSERVERCERTIFICATE": "yes",
        "CONNECTION_TIMEOUT": "30",
    }.get(key, "")

    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    result = extract_SQLserver.connect()
    assert result is not None

def test_disconnect():
    mock_engine = MagicMock()
    extract_SQLserver.disconnect(mock_engine)
    mock_engine.dispose.assert_called_once()

# def test_get_table_columns():
#     engine = extract_SQLserver.connect()
#     schema = 'dbo'
#     table = 'test_table'
#     result = extract_SQLserver.get_table_columns(schema, table, engine)
#     assert isinstance(result, pd.DataFrame)

# def test_extract_tables():
#     engine = extract_SQLserver.connect()
#     result = extract_SQLserver.extract_tables(engine)
#     assert result == True

# def test_main():
#     result = extract_SQLserver.main()
#     assert result == True
