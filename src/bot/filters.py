from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class NoStateFilter(Filter):
    """Пропускает только если у запроса нет никакого состояния"""

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return not (await state.get_state())
