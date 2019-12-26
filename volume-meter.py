import mido
import random
from time import sleep

row0 = (96, 97, 98, 99, 100, 101, 102, 103, 104)  # LED indices, first row
row1 = (112, 113, 114, 115, 116, 117, 118, 119, 120)  # LED incides, second row

VOLUME_SCALE = 2

def write_led(midi, led_id, color_vel):
    # color_vel is 0-15
    color_vel = (color_vel & 0b0011) + ((color_vel & 0b1100) << 2)
    midi.send(mido.Message("note_on", channel=0, note=led_id, velocity=color_vel))

STEPS = 16

def change_row(midi, volume: float, row):
    write_led(midi, row[-1], 15)
    row = row[:-1][::-1]
    for i in range(len(row)):
        v = (volume - i / len(row)) / (1 / len(row) / STEPS)
        write_led(midi, row[i], int(min(STEPS - 1, max(0, v))))

if __name__ == "__main__":
    import sys

    with mido.open_output("Launchkey Mini:Launchkey Mini MIDI 2 24:1") as midi:
        try:
            midi.send(
                mido.Message.from_bytes([0x90, 0x0C, 0x7F])
            )  # Switch to "InControl" mode
            for line in sys.stdin:
                ch0, ch1 = map(float, line.split())
                # print(ch0, ch1)
                change_row(midi, ch0 * VOLUME_SCALE, row0)
                change_row(midi, ch1 * VOLUME_SCALE, row1)
        except KeyboardInterrupt:
            pass
        finally:
            midi.send(
                mido.Message.from_bytes([0x90, 0x0C, 0x00])
            )  # Disable "InControl" mode
