# launchpad_art

Driving an original Novation Launchpad's LED grid directly over MIDI, for fun.

## Hardware

- Original Novation Launchpad (8x8 grid, an 8-button control row above it, an
  8-button scene column to the right)
- Connected over USB, visible to ALSA as a MIDI sequencer client named `Launchpad`

## Setup

```
sudo apt install python3-rtmidi
```

Note: if something else (e.g. a DAW/OSC bridge) already has the Launchpad's
raw MIDI device open exclusively, `python-rtmidi`'s ALSA sequencer backend
still works alongside it — sequencer ports allow multiple connected clients,
unlike the raw device.

## Files

- `launchpad.py` — the driver. `Launchpad` opens the MIDI in/out ports and
  exposes `led(x, y, color)` for the 8x8 grid (x,y = 0-7), `led(8, y, color)`
  for the right-hand scene column, `top_led(i, lit)` for the top control row,
  and `poll()` for non-blocking reads of button presses/releases.
- `icons.py` / `demo_icons.py` — a small library of 8x8 pixel-art icons
  (heart, invader, skull, smiley, flame, tree, creeper, lightning, check, x,
  mushroom) and a script that cycles through them on the hardware.
- `life.py` / `run_life.py` — Conway's Game of Life on the 8x8 grid with
  toroidal (wraparound) edges, run with `python3 run_life.py [seconds]`.

## Button naming convention

- Grid: `row, col`, 1-8, top-left is row 1 / col 1
- Top row: `Top-1` .. `Top-8`, left to right
- Right column: `Right-1` .. `Right-8`, top to bottom

## LED color byte

Velocity byte for `0x90` (note on) messages, bit layout per Novation's spec:

```
bit 6     = 0
bits 5..4 = green brightness (0-3)
bit 3     = clear the other buffer copy
bit 2     = write this data to both buffers
bits 1..0 = red brightness (0-3)
```

`launchpad.color(red, green)` builds this byte, always setting bits 2 and 3
so writes land as a steady (non-flashing) color.

## Game of Life controls

- Tap a dark pad: stamps a 3-cell blinker there (a lone cell would just die
  immediately, a blinker actually has a chance to persist)
- Tap a lit pad: kills that single cell
- `Top-8`: perturb — tops up any starving live cell (fewer than 2 neighbors)
  so it survives, then sprinkles in ~20 fresh random cells. Only ever adds
  cells, never removes any.
