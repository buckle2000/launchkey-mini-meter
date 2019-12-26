import mido
import random
from time import sleep
 
row1 = (96, 97, 98, 99, 100, 101, 102, 103, 104)  # LED indices, first row
row2 = (112, 113, 114, 115, 116, 117, 118, 119, 120)  # LED incides, second row
leds = row1 + row2  # LED indices, combined
 
 
def write_led(led_id, color_vel):
    midi_out.send(mido.Message('note_on', channel=0, note=led_id, velocity=color_vel))


def random_color():
    return random.randrange(127)
# 	red_or_green = bool(random.randint(0, 1))  # Making sure the number is always >0 for one component
# 	return random.randint(int(red_or_green), 3) + \
# 		   random.randint(int(not red_or_green), 3) * 16


if __name__ == "__main__":
    try:
        midi_out = mido.open_output('Launchkey Mini:Launchkey Mini MIDI 2 24:1')  # Launchkey InControl port

        midi_out.send(mido.Message.from_bytes([0x90, 0x0C, 0x7F]))  # Switch to "InControl" mode
    
        while True:
            color = int(input('Enter value:'))
            midi_out.send(mido.Message.from_bytes([0x90, 0x0C, 0x7F]))  # Switch to "InControl" mode
            
            for index, led in enumerate(row1):
                # Set current LED color
                write_led(row1[index], color)
                write_led(row2[index], color)
                
                # sleep(0.1)
 
    except KeyboardInterrupt:
        pass
 
 
for led in leds:
    write_led(led, 0)  # Turn off all LEDs
midi_out.send(mido.Message.from_bytes([0x90, 0x0C, 0x00]))  # Disable "InControl" mode
midi_out.close()