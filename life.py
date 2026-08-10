"""Conway's Game of Life on the 8x8 grid, toroidal (wraparound) edges."""
import random
from launchpad import color, OFF

SIZE = 8
BORN = color(0, 3)       # green: just born this generation
SURVIVOR = color(3, 3)   # amber: alive now, still alive next generation
DYING = color(3, 0)      # red: alive now, dies next generation


def random_grid(p=0.3):
    return [[random.random() < p for _ in range(SIZE)] for _ in range(SIZE)]


def count_neighbors(grid, x, y):
    n = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            if grid[(y + dy) % SIZE][(x + dx) % SIZE]:
                n += 1
    return n


def step(grid):
    new = [[False] * SIZE for _ in range(SIZE)]
    for y in range(SIZE):
        for x in range(SIZE):
            n = count_neighbors(grid, x, y)
            new[y][x] = (n in (2, 3)) if grid[y][x] else (n == 3)
    return new


TOP8_INDEX = 7  # Top-8, 0-indexed
RIGHT_COLUMN_X = SIZE  # scene column note-space x, one button per row

# A horizontal blinker: alone it oscillates forever rather than settling
# into a static still life, so a tap has a real chance of staying lively.
STAMP_OFFSETS = [(-1, 0), (0, 0), (1, 0)]


def stamp(grid, x, y):
    for dx, dy in STAMP_OFFSETS:
        grid[(y + dy) % SIZE][(x + dx) % SIZE] = True


def nudge_row_right(grid, y):
    """Shifts row y one cell to the right, wrapping around."""
    row = grid[y]
    grid[y] = [row[(x - 1) % SIZE] for x in range(SIZE)]


def perturb(grid, count=20):
    """Only ever adds cells, never removes any.

    First feeds any starving live cell (fewer than 2 neighbors) enough
    dead neighbors to reach 2, so nothing already alive dies of
    underpopulation from the perturb itself. Then sprinkles in fresh
    random cells for new activity.
    """
    for y in range(SIZE):
        for x in range(SIZE):
            if not grid[y][x]:
                continue
            deficit = 2 - count_neighbors(grid, x, y)
            if deficit <= 0:
                continue
            neighbor_coords = [
                ((x + dx) % SIZE, (y + dy) % SIZE)
                for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                if not (dx == 0 and dy == 0)
            ]
            dead_neighbors = [c for c in neighbor_coords if not grid[c[1]][c[0]]]
            random.shuffle(dead_neighbors)
            for nx, ny in dead_neighbors[:deficit]:
                grid[ny][nx] = True

    for _ in range(count):
        x = random.randrange(SIZE)
        y = random.randrange(SIZE)
        grid[y][x] = True


def apply_touches(lp, grid):
    """Drains pending controller events.

    A press on a dead grid pad stamps a small blinker there; a press on a
    live pad kills just that cell. A press on Top-8 injects random cells.
    A press on a right-hand scene button nudges that row right, wrapping.
    """
    while True:
        evt = lp.poll()
        if evt is None:
            return
        kind, pos, pressed = evt
        if not pressed:
            continue
        if kind == "grid":
            x, y = pos
            if x == RIGHT_COLUMN_X:
                nudge_row_right(grid, y)
            elif x < SIZE and y < SIZE:
                if grid[y][x]:
                    grid[y][x] = False
                else:
                    stamp(grid, x, y)
        elif kind == "top" and pos == TOP8_INDEX:
            perturb(grid)


def draw(lp, grid, next_grid, age):
    for y in range(SIZE):
        for x in range(SIZE):
            if not grid[y][x]:
                lp.led(x, y, OFF)
                continue
            if age[y][x] == 0:
                c = BORN
            elif next_grid[y][x]:
                c = SURVIVOR
            else:
                c = DYING
            lp.led(x, y, c)


def next_age(grid, next_grid, age):
    new_age = [[0] * SIZE for _ in range(SIZE)]
    for y in range(SIZE):
        for x in range(SIZE):
            if next_grid[y][x] and grid[y][x]:
                new_age[y][x] = age[y][x] + 1
    return new_age
