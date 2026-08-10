"""Driver for the original Novation Launchpad (8x8 grid + top CC row + right scene column)."""
import rtmidi

# Velocity byte flags (steady/non-flashing LED write)
_CLEAR_COPY = 0x0C

TOP_ROW_CCS = [104, 105, 106, 107, 108, 109, 110, 111]  # left to right


def color(red, green):
    """red/green each 0-3. Returns the velocity byte to write for a steady LED color."""
    red = max(0, min(3, red))
    green = max(0, min(3, green))
    return _CLEAR_COPY | (green << 4) | red


OFF = color(0, 0)
RED = color(3, 0)
RED_LOW = color(1, 0)
GREEN = color(0, 3)
GREEN_LOW = color(0, 1)
AMBER = color(3, 3)
YELLOW = color(2, 3)
ORANGE = color(3, 2)


class Launchpad:
    def __init__(self):
        self._out = rtmidi.MidiOut()
        self._in = rtmidi.MidiIn()
        ports = self._out.get_ports()
        idx = next(i for i, p in enumerate(ports) if p.startswith("Launchpad"))
        self._out.open_port(idx)

        in_ports = self._in.get_ports()
        in_idx = next(i for i, p in enumerate(in_ports) if p.startswith("Launchpad"))
        self._in.open_port(in_idx)
        self._in.ignore_types(sysex=True, timing=False, active_sense=True)

    def close(self):
        self._out.close_port()
        self._in.close_port()

    def reset(self):
        """Turns off all LEDs and resets device state."""
        self._out.send_message([0xB0, 0x00, 0x00])

    def led(self, x, y, c=GREEN):
        """x: 0-7 grid column, or 8 for the right-hand scene column. y: 0-7, top to bottom."""
        note = 16 * y + x
        self._out.send_message([0x90, note, c])

    def led_off(self, x, y):
        self.led(x, y, OFF)

    def top_led(self, i, lit=True):
        """i: 0-7 left to right, top control row."""
        self._out.send_message([0xB0, TOP_ROW_CCS[i], 127 if lit else 0])

    def poll(self):
        """Non-blocking. Returns (kind, index_or_xy, pressed) or None.
        kind is 'grid' with (x, y), or 'top' with i (0-7)."""
        msg = self._in.get_message()
        if msg is None:
            return None
        (status, data1, data2), _ = msg
        if status == 0xB0:
            i = TOP_ROW_CCS.index(data1) if data1 in TOP_ROW_CCS else None
            if i is None:
                return None
            return ("top", i, data2 > 0)
        if status in (0x90, 0x80):
            x = data1 % 16
            y = data1 // 16
            pressed = status == 0x90 and data2 > 0
            return ("grid", (x, y), pressed)
        return None
