import pytest
from datetime import datetime
from streamstats.analysis import Stats
from streamstats.models import Event


class TestStats:
    def make_event(self, level=20, source='api', ts=None):
        return Event(timestamp=ts or datetime(2024, 1, 1, 10, 0), level=level, source=source, message='test')

    def test_empty_stats(self):
        stats = Stats()
        d = stats.to_dict()
        assert d['total_events'] == 0
        assert d['time_range']['first'] is None

    def test_add_event(self):
        stats = Stats()
        stats.add_event(self.make_event(level=20, source='api'))
        stats.add_event(self.make_event(level=40, source='db'))
        assert stats.total_events == 2
        assert stats.levels['INFO'] == 1
        assert stats.sources['db'] == 1

    def test_error_sources(self):
        stats = Stats()
        stats.add_event(self.make_event(level=20, source='api'))
        stats.add_event(self.make_event(level=40, source='db'))
        stats.add_event(self.make_event(level=50, source='db'))
        assert stats.error_sources['db'] == 2
        assert 'api' not in stats.error_sources

    def test_time_range(self):
        stats = Stats()
        stats.add_event(self.make_event(ts=datetime(2024, 1, 1, 12, 0)))
        stats.add_event(self.make_event(ts=datetime(2024, 1, 1, 10, 0)))
        assert stats.first_timestamp == datetime(2024, 1, 1, 10, 0)
        assert stats.last_timestamp == datetime(2024, 1, 1, 12, 0)

    def test_skip_invalid(self):
        stats = Stats()
        stats.skip_invalid()
        stats.skip_invalid()
        assert stats.skipped_invalid_lines == 2

    def test_top_error_sources(self):
        stats = Stats()
        for _ in range(5):
            stats.add_event(self.make_event(level=40, source='db'))
        for _ in range(3):
            stats.add_event(self.make_event(level=40, source='api'))
        top = stats.top_error_sources(n=2)
        assert top[0] == {'source': 'db', 'count': 5}
        assert top[1] == {'source': 'api', 'count': 3}