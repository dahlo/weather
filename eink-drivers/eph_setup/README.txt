Unzip this folder into your /home/pi directory.
Type chmod +x eph_setup to make the script executable.
Type ./eph_setup
The script will update your Pi to the latest software, install
the software needed for your E-paper HAT, then reboot to activate.
Log back in and type sudo echo C >> /dev/epd/command and your screen should blank.
If not, check the fuse driver is running - type sudo service epd-fuse status.
You should get back '[ ok ] EPD FUSE is running.'
Then type cd gratis/PlatformWithOS/driver-common to move to the directory where the test programs live.
Now, if you type sudo ./epd_test_screen 2.7, you should see the screen clear and then display
Percheron Electronics. If you see no change in the display image but get the following message:

clear display
EPD panel broken
images start
image = 0
EPD panel broken

I'm afraid your screen has a crack in it and will not work. 

Please contact me at:

neil@percheron-electronics.uk

for further advice.


