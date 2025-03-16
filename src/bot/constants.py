# message texts
MAIN_MENU_MESSAGE = "Выберите, что хотите сделать."
START_MESSAGE = "<b>Привет. Это решение тестового задания в ТЕХНЕЗИС.</b>"
LOAD_SITES_EXCEL_FILE_MESSAGE = (
    "<b>Для того, чтобы добавить данные о сайтах - отправьте файл Excel.\n\n"
    "Вот некоторые ограничения к файлу:\n"
    "<i>- расширение должно быть xls либо xlsx;\n"
    "- таблица должна содержать 3 столбца: title (текст), url (корректный URL страницы), xpath (текст);\n"
    "- недопустимы пустые значения в ячейках.\n</i></b>"
)
INVALID_EXCEL_EXTENSIONS_MESSAGE = (
    "Вы прислали файл, у которого расширение {ext}. Допустимые расширения: {allowed_extensions}"
)
AFTER_LOADING_SITES_EXCEL_FILE_MESSAGE = "Отлично! Вот данные, которые были в файле: \n{data}"
AFTER_LOADING_SITES_EXCEL_FILE_NO_DATA_MESSAGE = (
    "Отлично! Только вы отправили файл, в котором нет данных ни об одном сайте.\n"
    "Если хотите еще раз - нажимайте кнопку."
)
AFTER_PARSE_TABLE_SITES_MESSAGE = (
    "<b>Вот средняя цена товара по каждому сайту.</b>\n\n"
    "{avg_prices}"
)
AVG_PRICE_TEMPLATE = "<b>{site}</b>: <i>{avg_price}</i>"

# button texts
LOAD_FILE_BTN = "Загрузить файл..."
PARSE_TABLE_SITES_BTN = "Спарсить данные с таблицы"
