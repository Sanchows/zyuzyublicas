from aiogram.fsm.state import State, StatesGroup


class FileGetting(StatesGroup):
    sites_file_choosing = State()
