from io import BytesIO
import logging

from db.connection import DatabaseConnection
from db.dals import SitesDAL
from db.schemas import SiteDTO
from files.excel import ExcelFile, SitesExcelReader
from files.exceptions import InvalidFileDataException, MissedRequiredColumnsException

logger = logging.getLogger(__name__)


async def load_sites_from_bytes_io(bytes_io: BytesIO) -> str:
    try:
        excel_reader = SitesExcelReader(file=ExcelFile(bytes_io))
    except MissedRequiredColumnsException as e:
        logger.error(e.message)
        raise e from None

    data_text = ""
    try:
        async with DatabaseConnection() as db:
            for site in excel_reader.read_sites():
                logger.debug("Записываем данные о сайте в БД: %s", site)
                await SitesDAL(db=db).insert(
                    item=SiteDTO(title=site.title, url=site.url, xpath=site.xpath)
                )
                data_text = (
                    f"{data_text}\n"
                    f"<b>title:</b> {site.title} | <b>url:</b> {site.url} | <b>xpath:</b> {site.xpath}"
                )
                logger.info("Данные о сайте успешно записаны в БД: %s", site)
    except InvalidFileDataException as e:
        logger.error(e.message)
        raise e from None

    return data_text
