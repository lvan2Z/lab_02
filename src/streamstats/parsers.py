import csv
import json

from errors import InvalidEventError


def parse_csv(file, file_name=None):
    reader = csv.DictReader(file)
    for line_number, row in enumerate(reader, start=2):
        if not any(v.strip() for v in row.values() if v):
            raise InvalidEventError("empty row", line_number, file_name)
        yield row


def parse_jsonl(file, file_name=None):
    for line_number, line in enumerate(file, start=1):
        if not line.strip():
            raise InvalidEventError("empty line", line_number, file_name)
        try:
            yield json.loads(line)
        except json.JSONDecodeError as e:
            raise InvalidEventError(str(e), line_number, file_name) from e
