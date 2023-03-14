# Enable interfaces on RPi

You have to enable the `SPI` and `I2C` interfaces of your Raspberry Pi.

```bash
sudo raspi-config
```

`Interface options -> SPI` and `Interface options -> I2C`

# Download drivers

From https://www.percheron-electronics.uk/support/software/

```bash
wget https://www.percheron-electronics.uk/wp-content/uploads/files/eph_setup.zip
unzip eph_setup.zip
cd eph_setup
chmod +x eph_setup
./eph_setup  # this step failed, but it downloaded a git repo etc
```

Contents of `eph_setup` if you can't find the zip file to download anymore:

```bash
#!/bin/bash
sudo apt-get update
yes | sudo apt-get upgrade
sudo apt-get -y install  libi2c-dev i2c-tools python-smbus libfuse-dev python-pil
git clone https://github.com/Percheron-Electronics/gratis2 gratis
cd gratis
make rpi
sudo make rpi-install
sudo reboot
```

# Install dependencies

Some of the packages were not found when running `eph_setup` as they have changed names etc.

```bash
sudo apt install libi2c-dev i2c-tools libfuse-dev

# some are pip packages now
sudo pip install smbus2 Pillow
```

The folder `/opt/vc` was missing for me, perhaps because I installed the minimal OS image. Get it through git instead,

```bash
# turns out this is a huge repo for the pi, takes ages. Better to download the code as a zip and extract it.
#git clone https://github.com/raspberrypi/firmware.git

wget https://github.com/raspberrypi/firmware/archive/refs/heads/master.zip
unzip master.zip

sudo cp -r firmware-master/opt/* /opt/
```


# Compile

The `make rpi` in `gratis/` still fails and says `undefined reference to "bcm_host_get_peripheral_address"`. A way around it was to copy the library flags to the end of the command line.

```bash
cd gratis
vim PlatformWithOS/driver-common/Makefile
```

and change all lines where `LDFLAGS` are being used so that `LDFLAGS` is at the end of the line.

```c
epd_fuse: ${FUSE_OBJECTS}
    ${CC} ${CFLAGS} ${LDFLAGS} -o "$@" ${FUSE_OBJECTS}
```

should be changed into

```c
epd_fuse: ${FUSE_OBJECTS}
    ${CC} ${CFLAGS} ${LDFLAGS} -o "$@" ${FUSE_OBJECTS} ${LDFLAGS}
```

Then continue installing

```bash
sudo make rpi-install
```


Reboot and it should start working. An issue I had was that only root was allowed to use the display. To get around that, change permissions of the `/dev/epd` mount point and restart the service:

```bash
sudo umount /dev/epd
sudo chmod a+rwx /dev/epd
sudo systemctl restart epd-fuse
```

After that I could run scripts as my own user.


# Using Python 2.7

I had scripts since before that used python2.7 to run. I decided to get those working first, before trying to update to python3.

```bash
sudo apt install python2.7 python2.7-dev
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python2.7 get-pip.py
python2.7 -m pip install Pillow
```

After this I was able to run the clock demo:

```bash
cd gratis/PlatformWithOS/demo
python2.7 ClockDemo.py
```



# Using Python 3.x

There were only minor fixes needed in `gratis/PlatformWithOS/demo/EPD.py` to get the display working using python3. Make the strings byte-strings before sending them as commands to the display,

```python
    def update(self):
        self._command('U')

    def partial_update(self):
        self._command('P')

    def clear(self):
        self._command('C')
```

just add a `b` infront of the string,

```python
    def update(self):
        self._command(b'U')

    def partial_update(self):
        self._command(b'P')

    def clear(self):
        self._command(b'C')
```
