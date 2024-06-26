# Weather forecase on E-ink display 

I have an e-ink display from [Percheron Electronics](https://www.percheron-electronics.uk/). It seems to be similar to the [PaPiRus](https://github.com/PiSupply/PaPiRus), but I have not tried to use their software to run my display. These scripts will fetch a weather forecast from [met.no Locationforecast API](https://api.met.no/weatherapi/locationforecast/2.0/documentation), create a plot of the data in a suitable size for the e-ink display and show the image on the display.

![](current_weather.dist.png)
# Usage

There are two scripts used; an R script to generate the forecast image, and a Python script to display the image on the e-ink display.

1. Generate the forecast image by giving the longitude and latitude to where you want to forecast:
```bash
Rscript generate_image.r 59.857958 17.637296
```
2. Display the image on the e-ink display:
```bash
python display_image.py current_weather.png
```

## Crontab

Add the following to your crontab to update the forecast automatically:

```bash
0 * * * * cd /path/to/weather ;  Rscript generate_image.r 59.857958 17.637296 ; python display_image.py current_weather.png
```

The script `print_ip.py` is a utility to print out the assigned IPs of the computer on the e-ink display. Add this to the crontab to print it at boot time:

```bash
@reboot    cd /path/to/weather ; sleep 10 ; python print_ip.py ; sleep 5 ; python display_image.py current_weather.png
```

# First time setup

## Setup the display and drivers

The installation script from the manufacturer did not work on my newly installed Raspberry Pi OS (2023-03-14) so I had to fiddle with it a bit before I got it up and running. Have a look at the [notes I made while installing](eink-drivers/install_log.md) for guidance if you have to do the same.

## Find coordinates for forcast

Use a map service, like [Google maps](https://www.google.com/maps) and find where you want to forecast the weather. If you click on a blank area on the map you will get a small box at the bottom of the map that displays the longitude and latitude of the point where you have clicked (e.g. [59.857958, 17.637296](https://goo.gl/maps/1n6ts7yJdZdySrAC7)).
 
# Install dependencies

A part from installing the drivers for the display, the python script only requires `Pillow`.

```bash
pip install Pillow
```

and the R script only needs `httr` and `jsonlite`.

```r
install.packages(c("httr", "jsonlite"))
```






