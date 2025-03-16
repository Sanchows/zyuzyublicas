from pathlib import Path

import aiosqlite

from settings import config


class DatabaseConnection:
    # TODO: переделать работу с БД так, чтобы можно было внедрить коннект БД в хэндлеры в качестве зависимости:
    #  либо через миддлвары либо через декоратор либо через сторонние решения.
    def __init__(self, path: Path = config.SQLITE_PATH):
        self.path = path

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.path)
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()
