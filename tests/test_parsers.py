import io
import pytest
from streamstats.parsers import parse_csv, parse_jsonl, get_parser
from streamstats.errors import InvalidEventError


class TestParseCSV:
    def test_valid_csv(self):
        data = "timestamp,level,source,message\n2024-01-01T10:00:00,INFO,api,ok\n"
        lines = list(parse_csv(io.StringIO(data)))
        assert len(lines) == 1
        assert lines[0][0] == 2
        assert lines[0][1]['level'] == 'INFO'

    def test_empty_file(self):
        assert list(parse_csv(io.StringIO(""))) == []

    def test_empty_row_raises(self):
        data = "timestamp,level,source,message\n,,,\n"
        with pytest.raises(InvalidEventError) as exc_info:
            list(parse_csv(io.StringIO(data), file_name="test.csv"))
        assert exc_info.value.line_number == 2
        assert exc_info.value.file_name == "test.csv"


class TestParseJSONL:
    def test_valid_jsonl(self):
        data = '{"timestamp": "2024-01-01T10:00:00", "level": "INFO", "source": "api", "message": "ok"}\n'
        lines = list(parse_jsonl(io.StringIO(data)))
        assert len(lines) == 1
        assert lines[0][0] == 1

    def test_empty_file(self):
        assert list(parse_jsonl(io.StringIO(""))) == []

    def test_empty_line_raises(self):
        data = '{"timestamp": "2024-01-01T10:00:00", "level": "INFO", "source": "a", "message": "1"}\n\n'
        with pytest.raises(InvalidEventError) as exc_info:
            list(parse_jsonl(io.StringIO(data), file_name="test.jsonl"))
        assert exc_info.value.line_number == 2

    def test_invalid_json_raises(self):
        data = '{"timestamp": "2024-01-01T10:00:00", "level": "INFO", "source": "a", "message": "ok"}\nnot json\n'
        with pytest.raises(InvalidEventError) as exc_info:
            list(parse_jsonl(io.StringIO(data), file_name="bad.jsonl"))
        assert exc_info.value.line_number == 2


class TestGetParser:
    def test_csv(self):
        assert get_parser('csv') is parse_csv

    def test_jsonl(self):
        assert get_parser('jsonl') is parse_jsonl

    def test_unsupported_raises(self):
        with pytest.raises(ValueError):
            get_parser('xml')