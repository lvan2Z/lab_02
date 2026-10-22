class StreamStatsError(Exception):
    pass

class InvalidEventError(StreamStatsError):
    def __init__(self, message, line_number=None, file_name=None):
        self.line_number = line_number
        self.file_name = file_name
        full_msg = "Invalid event"
        if file_name:
            full_msg += f" in {file_name}"
            if line_number:
                full_msg += f" at line {line_number}"
        full_msg += f": {message}"
        super().__init__(full_msg)
