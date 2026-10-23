import pytest
from datetime import datetime
from streamstats.models import Event, parse_event
from streamstats.errors import InvalidEventError, InvalidTimestampError


class TestParseEvent:
    def test_valid_event(self):
        data = {'timestamp': '2024-01-01T10:00:00', 'level': 'INFO', 'source': 'api', 'message': 'ok'}
        event = parse_event(data)
        assert event.timestamp == datetime(2024, 1, 1, 10, 0, 0)
        assert event.level == 20

    def test_missing_fields(self):
        with pytest.raises(InvalidEventError):
            parse_event({'timestamp': '2024-01-01T10:00:00'})

    def test_invalid_timestamp(self):
        data = {'timestamp': 'bad', 'level': 'INFO', 'source': 'api', 'message': 'ok'}
        with pytest.raises(InvalidTimestampError) as exc_info:
            parse_event(data, file_name='test.jsonl', line_number=5)
        assert exc_info.value.line_number == 5

    def test_invalid_level(self):
        data = {'timestamp': '2024-01-01T10:00:00', 'level': 'BLABLA', 'source': 'api', 'message': 'ok'}
        with pytest.raises(InvalidEventError):
            parse_event(data)

    def test_empty_source(self):
        data = {'timestamp': '2024-01-01T10:00:00', 'level': 'INFO', 'source': '   ', 'message': 'ok'}
        with pytest.raises(InvalidEventError):
            parse_event(data)
