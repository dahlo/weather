# Copyright 2013-2015 Pervasive Displays, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.


import sys
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from EPD import EPD

WHITE = 1
BLACK = 0

# fonts are in different places on Raspbian/Angstrom so search
possible_fonts = [
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
    '/usr/share/fonts/truetype/LiberationMono-Bold.ttf',              # B.B
    '/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf',              # B.B
    '/usr/share/fonts/TTF/FreeMonoBold.ttf',                          # Arch
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',                        # Arch
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
]


FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

if '' == FONT_FILE:
    raise 'no font file found'

CLOCK_FONT_SIZE = 40
DATE_FONT_SIZE  = 30

MAX_START = 0xffff

def main(argv):
    """main program - draw and display a test image"""

    epd = EPD()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog, f=epd.film))

    epd.clear()

    demo(epd)


def demo(epd):
    """simple partial update demo - draw draw a clock"""

    # initially set all white background
    image = Image.new('1', epd.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    clock_font = ImageFont.truetype(FONT_FILE, CLOCK_FONT_SIZE)
    date_font = ImageFont.truetype(FONT_FILE, DATE_FONT_SIZE)

    # clear the display buffer
    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    previous_second = 0
    previous_day = 0

    while True:
        while True:
            now = datetime.today()
            if now.second % 5 == 0:
                break
            time.sleep(0.5)

        if now.day != previous_day:
            draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
            draw.text((10, 55), '{y:04d}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=now.day), fill=BLACK, font=date_font)
            previous_day = now.day
        else:
            draw.rectangle((5, 10, width - 5, 10 + CLOCK_FONT_SIZE), fill=WHITE, outline=WHITE)

        draw.text((5, 10), '{h:02d}:{m:02d}:{s:02d}'.format(h=now.hour, m=now.minute, s=now.second), fill=BLACK, font=clock_font)

        # display image on the panel
        epd.display(image)
        if now.second < previous_second:
            epd.update()    # full update every minute
        else:
            epd.partial_update()
        previous_second = now.second

# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
