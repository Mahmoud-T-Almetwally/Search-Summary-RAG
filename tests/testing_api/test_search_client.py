from src.api import search_client
import requests

def test_get_search_results_success(mocker):
    """Tests the happy path where the API returns valid results."""
    # 1. Create fake API response data
    mock_response_data = {
        "organic_results": [
            {"position": 1, "title": "Result 1", "link": "http://test.com/1"},
            {"position": 2, "title": "Result 2", "link": "http://test.com/2"}
        ]
    }
    
    mock_get = mocker.patch('src.api.search_client.requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_data
    
    results = search_client.get_search_results("test query")
    
    assert len(results) == 2
    assert results[0]['link'] == "http://test.com/1"
    mock_get.assert_called_once()


def test_get_search_results_api_error(mocker):
    """Tests the failure path where the API returns an error."""
    mock_get = mocker.patch('src.api.search_client.requests.get')
    mock_get.side_effect = requests.exceptions.HTTPError
    
    results = search_client.get_search_results("test query")
    
    assert results == []