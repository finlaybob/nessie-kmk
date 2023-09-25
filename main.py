import os, time

import busio, board, displayio

import terminalio
from gc9a01 import GC9A01

from adafruit_display_text import label

import math, random, pwmio

from vectorio import Rectangle, Circle, Polygon

import rotaryio

enc = rotaryio.IncrementalEncoder(board.GP13, board.GP12, 2)
last_position = None

displayio.release_displays()

# create the spi device and pins we will need
spi = busio.SPI(board.GP10, MOSI=board.GP11)


while not spi.try_lock():
    print("spi no lock")
    pass
print("spi lock 👍")

spi.configure(baudrate=24000000)  # Configure SPI for 24MHz
spi.unlock()
cs = board.GP16
dc = board.GP12
reset = None #board.GP9

display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=reset)

display = GC9A01(display_bus, width=240, height=240)

# Make the display context
splash = displayio.Group()
display.show(splash)


color_bitmap = displayio.Bitmap(240, 240, 1)

color_palette = displayio.Palette(1)
color_palette[0] = 0x333333

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


rang = 1
for i in range(rang):
    sx = 119
    sy = 119
    circ_palette = displayio.Palette(1)
    circ_palette[0] = (0x33,0x33, 0xFF-(10*rang) + (10*i))
    #circ_palette[0] = 0x3333FF
    splash.append(Circle(pixel_shader=circ_palette, radius=120 - ((i-1)*int(120/float(rang))), x=sx, y=sy))

# Draw a label
text_group = displayio.Group(scale=1, x=120, y=25)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

v = 0.0
while True:
    v += 0.016
    text_group.x =  int(0.9 *(math.cos(v) * 119) + 113)
    text_group.y = int(0.9 *(math.sin(v) * 119) + 119)

    text_area.text = "{}".format(text_group.y)

    position = enc.position
    if last_position == None or position != last_position:
        print(position)
    last_position = position
    #print(position)
    time.sleep(1 / 60)
    display.refresh()
