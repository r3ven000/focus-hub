from core.habit_manager import HabitManager
from core.plugins import register

_HABIT_MANAGER: HabitManager = HabitManager(filename="habits.json")


@register(
    name=" habit tracker",
    key="h",
    description="Track and review your habits",
)
def habit_tracker(width: int | None = None) -> None:
    _HABIT_MANAGER.run(width)
