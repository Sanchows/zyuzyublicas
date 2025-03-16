import pathlib
from typing import Generator

import pandas as pd
from pydantic import ValidationError

from db.schemas import SiteDTO
from files.exceptions import (
    MissedRequiredColumnsException, InvalidFileDataException, InvalidFileExtensionException,
    NotCheckedFileException,
)
from files.files import File
from settings import config


class ExcelFile(File):
    extensions = config.EXCEL_EXTENSIONS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked = False
        self.check()

    def _check_extension(self):
        if isinstance(self.file, pathlib.Path):
            if (ext := self.file.suffix.lower()) not in self.extensions:
                raise InvalidFileExtensionException(f"Недопустимое расширение файла '{ext}'")

    def check(self):
        self._check_extension()
        self.checked = True

    @property
    def data_frame(self):
        if self.checked is False:
            raise NotCheckedFileException("Вызовите метод 'check()' перед получением data_frame")
        return pd.read_excel(self.file)


class ExcelReader:
    def __init__(self, file: ExcelFile):
        self.file = file

    def read(self):
        for row in self._iterrows():
            yield row

    def _iterrows(self):
        for n, row in self.file.data_frame.iterrows():
            yield n, row


class SitesExcelReader(ExcelReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check()

    def _check_required_columns(self):
        # Проверка наличия необходимых столбцов
        required_columns = {'title', 'url', 'xpath'}
        if not required_columns.issubset(self.file.data_frame.columns):
            missing_columns = required_columns - set(self.file.data_frame.columns)
            missing_columns_text = ", ".join(missing_columns)
            raise MissedRequiredColumnsException(
                f"В файле отсутствуют необходимые столбцы: {missing_columns_text}"
            )

    def check(self):
        self._check_required_columns()

    def read_sites(self) -> Generator[SiteDTO, None, None]:
        for row in self.read():
            try:
                yield SiteDTO(
                    title=row[1]['title'],
                    url=row[1]['url'],
                    xpath=row[1]['xpath']
                )
            except ValidationError as e:
                raise InvalidFileDataException(
                    f"Ошибка при чтении excel файла на строке №{row[0]}: недопустимое значение"
                )
