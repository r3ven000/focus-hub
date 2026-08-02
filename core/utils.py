import os
import re
import time
from pyfiglet import Figlet

figlet = Figlet(font='big')

def clear_screen() -> None:
#Clears the terminal screen depending on the operating system.
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width() -> int:
    return os.get_terminal_size().columns

def in_dev(*args, **kwargs):
    width = os.get_terminal_size().columns
    print('function in dev!'.center(width))

def timer(minutes, width):
    end_time = time.time() + (minutes * 60)
    while time.time() < end_time:
        try:
            remaining = end_time - time.time()
            mins, secs = divmod(int(remaining), 60)
            timer_str = f'remaining: {mins:02d}:{secs:02d}'
        
            os.system('cls' if os.name == 'nt' else 'clear')
            width = os.get_terminal_size().columns
            print('\n' * 3)
            ascii_time = figlet.renderText(f'{mins:02d}:{secs:02d}')
            for line in ascii_time.split('\n'):
                if line.strip():
                    print(line.center(width))
            time.sleep(0.5)
        except KeyboardInterrupt: 
            break
    print("time's up".center(width))
    time.sleep(1)


ANSI_RE = re.compile(r'\x1b\[[0-9;]*m', re.UNICODE)


def center_line(text: str, width: int) -> str:
    visible = ANSI_RE.sub('', text).rstrip('\n')
    pad = max(0, (width - len(visible)) // 2)
    return ' ' * pad + text
  
