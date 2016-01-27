#!/bin/sh

## Buendia Yocto setup script

#### Connect to internet

# echo "NETWORKING_AP=0
# NETWORKING_DHCP_DNS_SERVER=0
# NETWORKING_SSID=yourwifinetwork
# NETWORKING_PASSWORD=yourwifinpassword" > /debian/usr/share/buendia/site/99-local

# reboot

#### Setup repos and libraries

echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf

echo "src all     http://iotdk.intel.com/repos/1.1/iotdk/all
src x86 http://iotdk.intel.com/repos/1.1/iotdk/x86
src i586    http://iotdk.intel.com/repos/1.1/iotdk/i586
src/gz all http://repo.opkg.net/edison/repo/all
src/gz edison http://repo.opkg.net/edison/repo/edison
src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" > /etc/opkg/base-feeds.conf

opkg update
opkg install libmraa0 git python-smbus nano
echo set const >> ~/.nanorc  # so nano reports line number

cd /home/root
git clone --recursive https://github.com/geotheory/server-status
mv server-status gpio
chmod -R 755 gpio

cd gpio/libraries/Adafruit_Nokia_LCD
python setup.py install
cd ../Adafruit_Python_GPIO
python setup.py install
cd /home/root/gpio

#### set RTC time
python systime/systime_set_rtc.py

#### SD card 

mkdir -p /debian/home/buendia/sd
ln -s /debian/home/buendia/sd /home/root/gpio/sd
touch sd/sd_not_mounted
mount /dev/mmcblk1p1 /debian/home/buendia/sd/ && touch sd/sd_mounted &

#### Boot script

mkdir /etc/init.d
cd /etc/init.d
cp /home/root/gpio/boot_script.sh ./

update-rc.d boot_script.sh defaults 99

#### Finish

# rm /debian/usr/share/buendia/site/99-local
# reboot

