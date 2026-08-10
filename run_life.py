import sys
import time
from launchpad import Launchpad
from life import SIZE, random_grid, step, apply_touches, draw, next_age

GEN_INTERVAL = 0.4   # seconds between generations
POLL_SLICE = 0.05    # how often we check the controller for touches within that interval
RUN_SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 60


def main():
    lp = Launchpad()
    lp.reset()

    grid = random_grid()
    age = [[0] * SIZE for _ in range(SIZE)]
    draw(lp, grid, step(grid), age)  # show the initial seed immediately

    end_time = time.time() + RUN_SECONDS
    try:
        while time.time() < end_time:
            elapsed = 0.0
            while elapsed < GEN_INTERVAL:
                apply_touches(lp, grid)
                time.sleep(POLL_SLICE)
                elapsed += POLL_SLICE

            next_grid = step(grid)
            draw(lp, grid, next_grid, age)
            age = next_age(grid, next_grid, age)
            grid = next_grid
    finally:
        lp.reset()
        lp.close()


if __name__ == "__main__":
    main()
