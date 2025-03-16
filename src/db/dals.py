import asyncio
import logging
from typing import Generator

import aiosqlite

from db.schemas import SiteDTO, ReadOnlySiteDTO

logger = logging.getLogger(__name__)


class SitesDAL:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db
        # нужно ставить lock для предотвращения переключения async контекста во время запросов, так как у нас SQLite
        self.lock = asyncio.Lock()

    async def select(self) -> Generator[ReadOnlySiteDTO, None, None]:
        async with self.lock:
            query = "SELECT id, title, url, xpath FROM sites"
            async with self.db.execute(query) as cursor:
                async for row in cursor:
                    yield ReadOnlySiteDTO(id=row[0], title=row[1], url=row[2], xpath=row[3])

    async def insert(self, item: SiteDTO):
        async with self.lock:
            async with self.db.cursor() as cursor:
                query = "INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)"
                await cursor.execute(
                    query,
                    (item.title, str(item.url), item.xpath)
                )
                await self.db.commit()

    def update(self, pk: int, updated_data: SiteDTO):
        pass

    def delete(self, pk: int):
        pass
