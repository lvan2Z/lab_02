import logging

from .models import LEVEL_NAMES


class Stats:
    def __init__(self):
        self.total_events = 0
        self.levels = {}
        self.sources = {}
        self.error_sources = {}
        self.first_timestamp = None
        self.last_timestamp = None
        self.skipped_invalid_lines = 0

    def add_event(self, event):
        self.total_events += 1

        level_name = LEVEL_NAMES[event.level]
        self.levels[level_name] = self.levels.get(level_name, 0) + 1
        self.sources[event.source] = self.sources.get(event.source, 0) + 1

        if event.level >= logging.ERROR:
            self.error_sources[event.source] = self.error_sources.get(event.source, 0) + 1

        if (not self.first_timestamp) or event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp
        if (not self.last_timestamp) or event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp

    def skip_invalid(self):
        self.skipped_invalid_lines += 1

    def top_error_sources(self, n=5):
        ordered = sorted(
            self.error_sources.items(),
            key=lambda item: (-item[1], item[0]),
        )
        return [
            {'source': source, 'count': count}
            for source, count in ordered[:n]
        ]

    def to_dict(self):
        return {
            'total_events': self.total_events,
            'levels': dict(self.levels),
            'sources': dict(self.sources),
            'top_error_sources': self.top_error_sources(),
            'time_range': {
                'first': self.first_timestamp.isoformat() if self.first_timestamp else None,
                'last': self.last_timestamp.isoformat() if self.last_timestamp else None,
            },
            'skipped_invalid_lines': self.skipped_invalid_lines,
        }