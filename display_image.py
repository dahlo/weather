# Copyright 2013-2015 Pervasive Displays, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.


import sys
import os
import time
from PIL import Image
from PIL import ImageOps
from EPD import EPD


def main(filename, rotation_degrees=None):
    """main program - display image"""

    # print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog, f=epd.film))

    # open image and convert to grayscale
    image = Image.open(sys.argv[1])
    image = ImageOps.grayscale(image)

    # if rotation
    if rotation_degrees:
        image = image.rotate(rotation_degrees)

    # convert to 8-bit format
    bw = image.convert("1", dither=Image.FLOYDSTEINBERG)

    # display the image
    epd = EPD()
    epd.display(bw)
    epd.update()


# main
if "__main__" == __name__:
    
    # get file name
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit(f'Usage: {sys.argv[0]} <image path> [<degrees to rotate image>]')


    # get optional argument if present
    try:
        main(filename, int(sys.argv[2]))
    except IndexError:
        main(filename)

