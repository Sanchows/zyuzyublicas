import io
import pathlib


class File:
    def __init__(self, file: pathlib.Path | io.BytesIO):
        self.file = file
        self.checked = False
        self.check()

    def check(self):
        if isinstance(self.file, pathlib.Path):
            if not self.file.is_file():
                raise Exception(f'{self.file} is not a file')
        self.checked = True
