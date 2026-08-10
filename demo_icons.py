import time
from launchpad import Launchpad
from icons import ICONS, draw, clear_grid

lp = Launchpad()
lp.reset()
time.sleep(0.2)

for name in ICONS:
    print(name)
    draw(lp, name)
    time.sleep(1.2)
    clear_grid(lp)
    time.sleep(0.2)

lp.reset()
lp.close()
