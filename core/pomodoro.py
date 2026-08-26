from .arts import computer, coffee
from utils import timer
from .config import WORK_TIME, BREAK_TIME


def pomodoro(width):
    print("staeting session...".center(width))
    if not timer(WORK_TIME, width, art=computer):
        return
    print("starting break...".center(width))
    timer(BREAK_TIME, width, art=coffee)
