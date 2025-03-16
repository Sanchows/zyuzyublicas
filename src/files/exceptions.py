class MissedRequiredColumnsException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message

class InvalidFileDataException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message

class InvalidFileExtensionException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message

class NotCheckedFileException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
