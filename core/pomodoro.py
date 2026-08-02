from .utils import timer, get_terminal_width
from .config import WORK_TIME, BREAK_TIME

def pomodoro(width):
    width = get_terminal_width()
    print('starting work session...'.center(width))
    timer(WORK_TIME, width)
    print('starting break...'.center(width))
    timer(BREAK_TIME, width)
