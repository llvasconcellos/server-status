First we need to deactivate the Buendia Server to connect to LAN internet.  This is covered in more detail [here](https://github.com/projectbuendia/buendia/wiki/Setting-up-an-Edison).  To do this connect to the Edison using `screen`, as documented in setup.  You'll find yourself in _Yocto_ (NB. not the jailed Debian OS that Buendia runs on and is accessible via e.g. `chroot /home/root/debian/ /bin/bash` or directly via `ssh`; `screen` is recommended here as `ssh` will be disrupted).  Run the next 4 lines together:

    echo "NETWORKING_AP=0
    NETWORKING_DHCP_DNS_SERVER=0
    NETWORKING_SSID=your_network_id
    NETWORKING_PASSWORD=your_network_pwd" > /home/root/debian/usr/share/buendia/site/99-local
    
    reboot

When you're back up, test the internet with

    curl icanhazip.com


#### GPIO Setup

GPIO appears to only work from Yocto.  Yocto comes pre-installed with the necessary GPIO libraries, but does require an update.  Yocto's package manager (equivalent of `apt-get`) is `opkg`, and work's in pretty much the same way.

    opkg update
    opkg install libmraa0
    
    mkdir /home/root/gpio
    cd /home/root/gpio

Now let's test the GPIO.  Run the following 13 lines together:

    echo "import mraa
    import time
    
    # Setup
    x = mraa.Gpio(31)
    x.dir(mraa.DIR_OUT)
    
    # Loop
    while True:
        x.write(1)
        time.sleep(0.5)
        x.write(0)
        time.sleep(0.5)" > blink.py

Connect an LED to your Edison's GPIO Block - high to the `GP44` pin, low to `GND`  Make sure you add a resistor (e.g. 1k) in series to protect the LED.

    python blink.py

You should now be blinking.


### Buendia server status LED

For this we'll use the following pins to control an RGB LED. Note they're labelled differently on the GPIO block to the code:

| Label on GPIO Block  | pin # in code | RGB LED pin |
| ------------- | ------------- | ------------- |
| GP44  | 31  | red |
| GP45  | 45  | green |
| GP46  | 32  | blue |

Setup working folders

    mkdir /home/root/debian/home/buendia
    mkdir /home/root/debian/home/buendia/sd
    cd /home/root/debian/home/buendia

Mount SD card

Append a line to debian's /etc/rc.local file (before 'exit') to mount the SD at /home/buendia/sd on startup

    chroot /home/root/debian perl -0777 -i -pe 's/^exit 0/# mount SD card\nmount \/dev\/mmcblk1p1 \/home\/buendia\/sd\/ &\n\nexit 0/igm' /etc/rc.local

Check it looks right - should see `mount /dev/mmcblk1p1 /home/buendia/sd/ &` above `exit 0`

    tail /home/root/debian/etc/rc.local

Symbolic folder from Yocto to debian SD card folder

    ln -s /home/root/debian/home/buendia/sd /home/root/gpio/sd

Get the server-reporting Python script

    chroot /home/root/debian git clone https://github.com/geotheory/buendia_server_status
    cp buendia_server_status/server_status.py /home/root/gpio
    chmod 755 /home/root/gpio/server_status.py

Now we'll configure the Python script to run on startup.  This means creating a `.sh` file that will call it, and telling Yocto to execute at startup.

    mkdir /etc/init.d
    cd /etc/init.d
    
    echo "#!/bin/sh
    mount /dev/mmcblk1p1 /home/root/debian/home/buendia/sd/
    python /home/root/gpio/server_status.py >> /home/root/gpio/sd/log.txt 2>&1" > server_status.sh
    
    chmod 755 server_status.sh

Add script to update-rc.d daemon

    update-rc.d server_status.sh defaults 99


### Battery status LED

For an LED to report on battery level you'll need to purchase the [SparkFun LiPo Fuel Gauge](https://www.sparkfun.com/products/10617).

We'll use the following pins to control an RGB LED. Note again they're labelled differently on the GPIO block to the code:

| Label on GPIO Block  | pin # in code | RGB LED pin |
| ------------- | ------------- | ------------- |
| GP131  | 35  | red |
| GP130  | 26  | green |
| GP129  | 25  | blue |

[WORK IN PROGRESS..]


### Reinstating the Buendia server

Setup is now complete.  Connect LED's to the GPIO as per the table above. Then revert the system to server mode:

    rm /home/root/debian/usr/share/buendia/site/99-local
    reboot

You should now see the LED's flicker to test, and then begin reporting server status

