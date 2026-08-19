from unittest.mock import patch, Mock
from extractor.api_client import APIClient

def test_get_users_returns_data_on_success():
    client = APIClient("https://fake-api.com")

    fake_response = Mock()
    fake_response.json.return_value = [{"id": 1, "name": "Test User"}]
    fake_response.raise_for_status.return_value = None

    with patch("extractor.api_client.requests.get", return_value=fake_response):
        result = client.get_users()

    assert result == [{"id": 1, "name": "Test User"}]