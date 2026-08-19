# automated checks confirming validate_users() correctly accepts good data and rejects bad data.
from extractor.models import validate_users

def test_valid_record_passes():
    data = [{"id": 1, "name": "Aayusha", "email": "a@example.com", "phone": "123"}]
    result = validate_users(data)
    assert len(result) == 1
    assert result[0]["name"] == "Aayusha"

def test_invalid_record_is_skipped():
    data = [{"id": "not-a-number", "name": "Bad", "email": "b@example.com", "phone": "123"}]
    result = validate_users(data)
    assert len(result) == 0
