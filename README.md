# Weather forecase on E-ink display

I have an e-ink display from [Percheron Electronics](https://www.percheron-electronics.uk/). It seems to be similar to the [PaPiRus](https://github.com/PiSupply/PaPiRus), but I have not tried to use their software to run my display.

# Usage

There are two scripts used; an R script to generate the forecast image, and a Python script to display the image on the e-ink display.

1. Generate the forecast image by giving the longitude and latitude to where you want to forecast:
    Rscript generate_image.r 59.857958 17.637296
2. Display the image on the e-ink display:
    python display_image.py current_weather.png

# First time setup

## Setup the display and drivers

The installation script from the manufacturer did not work on my newly installed Raspberry Pi OS (2023-03-14) so I had to fiddle with it a bit before I got it up and running. Have a look at the [notes I made while installing](eink-drivers/install_log.md) for guidance if you have to do the same.

## Find coordinates for forcast

Use a map service, like [Google maps](https://www.google.com/maps) and find where you want to forecast the weather. If you click on a blank area on the map you will get a small box at the bottom of the map that displays the longitude and latitude of the point where you have clicked (e.g. [59.857958, 17.637296](https://goo.gl/maps/1n6ts7yJdZdySrAC7)).
 







