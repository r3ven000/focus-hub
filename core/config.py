#POMOTRACK Project Settings and Constants
import os
import re
import subprocess

text = "FOCUS-HUB"
# Ваш кастомный градиент (Синий -> Голубой -> Белый -> Серый)
custom_colors = "grad-blue"

# Берем текущее окружение системы и принудительно включаем цвет
env = os.environ.copy()
env["FORCE_COLOR"] = "3"

result = result = subprocess.run(
    ["npx", "oh-my-logo@latest", text, custom_colors,
     "--filled", "--block-font", "block", "--letter-spacing", "0"],
    capture_output=True,
    text=True,
    encoding="utf-8",
    env=env,  # Передаем обновленное окружение с включенным цветом
    check=True,
)

WELCOME_ART = result.stdout
WORK_TIME = 25
BREAK_TIME = 5

ITEMS_MENU = [ 
    ('⏱  pomodoro timer', 'p'),
    (' to-do', 't'),
    (' habbit-tracker', 'h'),
    (' diary', 'd'),
    ('  import-data-to-.json', 'j'),
    (' import-data-to-Obsidian', 'o'),
    (' settings', 's'),
    (' quit', 'q')
]

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m', re.UNICODE)

def center_line(text: str, width: int) -> str:
    visible = ANSI_RE.sub('', text).rstrip('\n')
    pad = max(0, (width - len(visible)) // 2)
    return ' ' * pad + text
