from unittest.mock import patch, MagicMock
import source.extract_SQLserver as extract_SQLserver
import pandas as pd



def test_init():
    result = extract_SQLserver.init()
    assert result == True

# def test_generate_sas_token():
#     result = extract_SQLserver.generate_sas_token()
#     assert result == True

# def test_get_sas_token_from_file():
#     result = extract_SQLserver.get_sas_token_from_file()
#     assert result == "https://datalakeblob.blob.core.windows.net/datalakeblob?sp=rl&st=2022-02-15T16:15:00Z&se=2022-02-15T17:15:00Z&sv=2020-08-04&sr=c&sig=J"

# def test_main():
#     with patch('source.extract_SQLserver.extract_data') as mock_extract_data:
#         mock_extract_data.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
#         result = extract_SQLserver.main()
#         assert result == True
#         mock_extract_data.assert_called_once()