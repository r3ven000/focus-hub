import os
import re
import time
from pyfiglet import Figlet
import sys

figlet = Figlet(font="roman")
computer = r"""





                       .,,uod8B8bou,,.
              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.
         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||
         !...:!TVBBBRPFT||||||||||!!^^""'   ||||
         !.......:!?|||||!!^^""'            ||||
         !.........||||                     ||||
         !.........||||  ##                 ||||
         !.........||||                     ||||
         !.........||||                     ||||
         !.........||||                     ||||
         !.........||||                     ||||
         `.........||||                    ,||||
          .;.......||||               _.-!!|||||
   .,uodWBBBBb.....||||       _.-!!|||||||||!:'
!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....
!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.
!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.
!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^"`;:::       `.
!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.
`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo.
  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'
    `........::::::::::::::::;iof688888888888888888888b.     `
      `......:::::::::;iof688888888888888888888888888888b.
        `....:::;iof688888888888888888888888888888888899fT!
          `..::!8888888888888888888888888888888899fT|!^"'
            `' !!988888888888888888888888899fT|!^"'
                `!!8888888888888888899fT|!^"'
                  `!988888888899fT|!^"'
                    `!9899fT|!^"'
                      `!^"'






"""


def clear_screen() -> None:
    # Clears the terminal screen depending on the operating system.
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def get_terminal_width() -> int:
    return os.get_terminal_size().columns


def in_dev(*args):
    width = os.get_terminal_size().columns
    print("function in dev!".center(width))


def timer(minutes, width):
    end_time = time.time() + (minutes * 60)
    while time.time() < end_time:
        try:
            remaining = end_time - time.time()
            mins, secs = divmod(int(remaining), 60)

            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.flush()
            width = os.get_terminal_size().columns
            print("\n" * 3)
            ascii_time = figlet.renderText(f"{mins:02d}:{secs:02d}")
            for line in ascii_time.split("\n"):
                if line.strip():
                    print(line.center(width))
            art_lines = [l for l in computer.split("\n") if l.strip()]
            pad = max(0, (width - max(len(l) for l in art_lines)) // 2)
            for l in art_lines:
                print(" " * pad + l)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    print("time's up".center(width))
    time.sleep(1)


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m", re.UNICODE)


def center_line(text: str, width: int) -> str:
    visible = ANSI_RE.sub("", text).rstrip("\n")
    pad = max(0, (width - len(visible)) // 2)
    return " " * pad + text


def lerp_color(hex_start, hex_end, t):
    start = [int(hex_start[i : i + 2], 16) for i in (1, 3, 5)]
    end = [int(hex_end[i : i + 2], 16) for i in (1, 3, 5)]
    rgb = tuple(round(a + (b - a) * t) for a, b in zip(start, end))
    return rgb


def colorize(text, r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"
