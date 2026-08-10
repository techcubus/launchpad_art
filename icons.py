"""Small 8x8 icon library for the Launchpad (red/green/amber only, no blue).

Each icon is 8 rows of 8 characters:
  . = off   r = red     R = red low
            g = green   G = green low
            a = amber   A = amber low
"""
from launchpad import color

_LEGEND = {
    ".": (0, 0),
    "r": (3, 0), "R": (1, 0),
    "g": (0, 3), "G": (0, 1),
    "a": (3, 3), "A": (1, 1),
}

ICONS = {
    "heart": [
        ".rr..rr.",
        "rrrrrrrr",
        "rrrrrrrr",
        "rrrrrrrr",
        ".rrrrrr.",
        "..rrrr..",
        "...rr...",
        "........",
    ],
    "invader": [
        "..g..g..",
        "..g..g..",
        "..gggg..",
        ".gggggg.",
        "gg.gg.gg",
        "gggggggg",
        "g.gggg.g",
        "g.g..g.g",
    ],
    "skull": [
        ".aaaaaa.",
        "aaaaaaaa",
        "aa.aa.aa",
        "aaaaaaaa",
        ".aaaaaa.",
        ".a.aa.a.",
        "a.aaaa.a",
        ".aa..aa.",
    ],
    "smiley": [
        "..aaaa..",
        ".a....a.",
        "a.a..a.a",
        "a......a",
        "a.a..a.a",
        "a..aa..a",
        ".a....a.",
        "..aaaa..",
    ],
    "flame": [
        "...a....",
        "..aaa...",
        "..rrr...",
        ".rrrrr..",
        ".rrrrr..",
        "rrrrrrr.",
        "rrrrrrr.",
        ".rrrrr..",
    ],
    "tree": [
        "...g....",
        "..ggg...",
        ".ggggg..",
        "..ggg...",
        ".ggggg..",
        "ggggggg.",
        "...R....",
        "...R....",
    ],
    "creeper": [
        "gggggggg",
        "gggggggg",
        "gg.gg.gg",
        "gg.gg.gg",
        "ggg..ggg",
        "gg....gg",
        "g......g",
        "gg....gg",
    ],
    "lightning": [
        "...aa...",
        "..aa....",
        ".aa.....",
        "aaaaaaa.",
        "....aa..",
        "...aa...",
        "..aa....",
        ".aa.....",
    ],
    "check": [
        "........",
        ".......g",
        "......g.",
        ".....g..",
        "g...g...",
        ".g.g....",
        "..g.....",
        "........",
    ],
    "x": [
        "r......r",
        ".r....r.",
        "..r..r..",
        "...rr...",
        "...rr...",
        "..r..r..",
        ".r....r.",
        "r......r",
    ],
    "mushroom": [
        "..rrrr..",
        ".rrrrrr.",
        "rrrrrrrr",
        "rrrrrrrr",
        "..A..A..",
        "..A..A..",
        "..A..A..",
        ".AAAAAA.",
    ],
}


def draw(lp, name):
    pattern = ICONS[name]
    for y, row in enumerate(pattern):
        for x, ch in enumerate(row):
            red, green = _LEGEND[ch]
            lp.led(x, y, color(red, green))


def clear_grid(lp):
    for y in range(8):
        for x in range(8):
            lp.led_off(x, y)
