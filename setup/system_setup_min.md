## Buendia Yocto quick setup

#### Connect to internet

    echo "NETWORKING_AP=0
    NETWORKING_DHCP_DNS_SERVER=0
    NETWORKING_SSID=yourwifinetwork
    NETWORKING_PASSWORD=yourwifinpassword" > /debian/usr/share/buendia/site/99-local

    reboot

#### Setup repos and libraries

    echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
    echo "src all     http://iotdk.intel.com/repos/1.1/iotdk/all
    src x86 http://iotdk.intel.com/repos/1.1/iotdk/x86
    src i586    http://iotdk.intel.com/repos/1.1/iotdk/i586" > /etc/opkg/base-feeds.conf
    opkg update
    opkg install libmraa0 git python3-smbus flex bison

    cd /home/root
    git clone https://github.com/geotheory/server-status
    mv server-status gpio
    chmod -R 755 gpio

    cd gpio/libraries/Adafruit_Nokia_LCD
    python setup.py install
    cd ../Adafruit_Python_GPIO
    python setup.py install
    cd ../..

#### SD card 

    mkdir /debian/home/buendia
    mkdir /debian/home/buendia/sd
    mount /dev/mmcblk1p1 /debian/home/buendia/sd/
    ln -s /debian/home/buendia/sd /home/root/gpio/sd

#### Boot script

    mkdir /etc/init.d
    cd /etc/init.d
    cp /home/root/gpio/boot_script.sh ./

    update-rc.d boot_script.sh defaults 99


#### Finish

    rm /debian/usr/share/buendia/site/99-local
    reboot

