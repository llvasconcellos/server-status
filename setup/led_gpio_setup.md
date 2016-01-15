## GPIO LED setup instructions

The following instructions detail the steps to setup your Intel Edison to report on Edison's server and battery charge statuses.  These reporting systems can be individually deactivated if your preferred configuration is for just one - see [startup configuration](#startup-configuration) below.

--------------------------


#### Connect to the internet

First we need to deactivate the Buendia Server to connect to LAN internet.  This is covered in more detail [here](https://github.com/projectbuendia/buendia/wiki/Setting-up-an-Edison).  To do this connect to the Edison using `screen`, as documented in setup.  You'll find yourself in _Yocto_, the branch of Linux designed for embedded projects like Edison.

(NB. note that OpenMRS (Buendia) runs on a 'jailed' Debian OS which runs independently on top of Yocto. Its file system is accessible from Yocto via the path `/home/root/debian` or the symlink (shortcut) folder `/debian`.  You can access Debian using a `chroot` operation (e.g. `chroot /debian /bin/bash`) or directly via `ssh` when the Buendia server is up and configured as an Access Point.)

Run the next 4 lines together to deactivate the Buendia server and connect to internet via local wifi:

    echo "NETWORKING_AP=0
    NETWORKING_DHCP_DNS_SERVER=0
    NETWORKING_SSID=yourwifinetwork
    NETWORKING_PASSWORD=yourwifinpassword" > /debian/usr/share/buendia/site/99-local
    
    reboot

When you're back up you can test the internet with `curl icanhazip.com`.  Don't forget that Buendia needs to be reinstated after setting up the LED reporting - see instructions at the bottom.

--------------------------


#### GPIO Setup

GPIO appears to only work from Yocto.  Yocto comes pre-installed with the necessary GPIO libraries, but does require an update.  Yocto's package manager (equivalent of `apt-get`) is `opkg`, and work's in pretty much the same way.

    echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
    echo "src all     http://iotdk.intel.com/repos/1.1/iotdk/all
    src x86 http://iotdk.intel.com/repos/1.1/iotdk/x86
    src i586    http://iotdk.intel.com/repos/1.1/iotdk/i586" > /etc/opkg/base-feeds.conf
    opkg update
    opkg install libmraa0 git flex bison

Get the LED scripts that will work with the GPIO.  This requires `chroot` as git is only on Debian side.

    cd /home/root
    chroot /debian git clone https://github.com/geotheory/server-status
    mv /debian/server-status /home/root/gpio
    chmod -R 755 gpio
    cd gpio

Next mount the SD card to Debian (first manually) and setup symlinks so we can use it in Yocto.

    mkdir /debian/home/buendia
    mkdir /debian/home/buendia/sd
    mount /dev/mmcblk1p1 /debian/home/buendia/sd/
    ln -s /debian/home/buendia/sd /home/root/gpio/sd

Automating the SD mounting is done by the _boot script_ that we implement next.

--------------------------


#### Startup configuration

Now we'll configure a script to run on startup to which we can add our commands to run the LED python scripts.  This means creating a `.sh` file in `/etc/init.d` and telling Yocto to run it at startup:

    mkdir /etc/init.d
    cd /etc/init.d
    cp /home/root/gpio/boot_script.sh ./

Yocto launches the script on startup if it has been added to the `update-rc.d daemon`:

    update-rc.d boot_script.sh defaults 99

If you need to remove this script from the daemon at a later point the command is `update-rc.d -f boot_script.sh remove`.

If you prefer to only report on server status but not battery status, just edit `/etc/init.d/boot_script.sh` to comment out the line that calls `battery_status.py`.  And vice versa to remove server status.

--------------------------


### Server Status LED

For server status we'll use the following pins to control an RGB LED (common cathode type). Note they're labelled differently on the GPIO block to the code:

| Label on GPIO Block  | pin # in code | RGB LED pin |
| ------------- | ------------- | ------------- |
| GP44  | 31  | red |
| GP45  | 45  | green |
| GP46  | 32  | blue |


This shows the schematic layout for the circuit.

![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/Buendia-server.svg)

(Schematic available to edit at [digikey.com](https://www.digikey.com/schemeit/#28q8))

Once connected you can test the circuit by manually running the `test_server_leds.py` script in the `test_scipts folder`.  If that works you're set up and on reboot the system should report.

#### Colour codes

The server-status LED reports Buendia's status in the following ways.  Some of these are determined 'externally' by Yocto and some by the status code that is output 'internally' from Buendia.

| State                          | Colour |
| -------------                  | ------------- |
| booting                        | blinking blue/green slowly |
| Tomcat up                      | blinking blue/green fast |
| OpenMRS up                     | green |
| Internal check: server down    | blinking red very slowly |
| Internal check: server up      | green |
| Internal check: backup started | blinking blue slowly |
| Internal check: backing-up     | blinking blue fast |
| Internal check: backup failed  | blinking blue/red very slowly |
| Update: checking for updates   | blinking green slow |
| Update: updating               | blinking green fast |
| Update: update failed          | blinking green/red very slowly |
| Server LED script failure      | flashing red (very briefly) every few seconds|

--------------------------


### Battery Status LED

For an LED to report on battery level you'll need to purchase the [SparkFun LiPo Fuel Gauge](https://www.sparkfun.com/products/10617), as well as the [Sparkfun I2C Block](https://www.sparkfun.com/products/13034) to speak to it - see [hardware setup instructions](./hardware_setup.md).

We'll use the following pins to control the LED. Note again they're labelled differently on the GPIO block to the code:

| Label on GPIO Block  | pin # in code | RGB LED pin |
| ------ | --- | ----- |
| GP131  | 35  | red   |
| GP130  | 26  | green |
| GP129  | 25  | blue  |

This shows the schematic layout for the system's two circuits:

![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/Buendia-battery.svg)

(Schematic available to edit at [digikey.com](https://www.digikey.com/schemeit/#28rf))

Connect the 2000mAh battery, the LiPi Fuel Gauge and the I2C Block as per the circuit diagram above.  Remove the 400 mAh battery that comes with the Battery Block, and solder in place GPIO header pins to link to the Fuel Gauge.  We recommend using detatchable connectors and jumper leads so the Edison stack or battery can be easily accessed if necessary.

#### Colour codes

The battery-status LED reports battery charge level as follows:

| Charge     | Colour |
| ---------- | ------ |
| Over 75%   | green  |
| 50% - 75%  | blue   |
| 25% - 50%  | red    |
| Under 25%  | blinking red (gets faster) |
| Battery LED script failure | flashing red (very briefly) every few seconds |

--------------------------


### Reinstating the Buendia server

Setup is now complete.  Connect LED's to the GPIO as per the table above. Then revert the system to server mode:

    rm /debian/usr/share/buendia/site/99-local
    reboot

You should now see the LEDs you've enacted in operation.

