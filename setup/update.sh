#!/bin/sh

## Buendia Yocto setup script
## Use this when manually updating an Edison that has previously had Yocto server-status set up
## N.B. This just updates reporting scripts, not RTC clock time or libraries

#### To connect to internet if necessary

# echo "NETWORKING_AP=0
# NETWORKING_DHCP_DNS_SERVER=0
# NETWORKING_SSID=yourwifinetwork
# NETWORKING_PASSWORD=yourwifinpassword" > /debian/usr/share/buendia/site/99-local
# reboot

echo '1/3: CLONE SERVER-STATUS REPO'
cd /home/root
rm -rf server-status
rm -rf gpio_old
git clone https://github.com/projectbuendia/server-status
mv gpio gpio_old || echo 'no existing gpio folder'
cp -R server-status gpio
chmod -R 755 gpio
cd gpio

#### SD card 
echo '2/3: MOUNT S.D. CARD'
umount /dev/mmcblk1p1 &                 # unmount if already mounted
mkdir -p /debian/home/buendia/sd/logs   # in case SD fails sometime
ln -s /debian/home/buendia/sd /home/root/gpio/sd
touch sd/sd_not_mounted
mount /dev/mmcblk1p1 /debian/home/buendia/sd/ && touch sd/sd_mounted &
mkdir -p /debian/home/buendia/sd/logs

#### Boot script
echo '3/3: SET UP BOOT SCRIPT'
mkdir -p /etc/init.d
cd /etc/init.d
cp /home/root/gpio/boot_script.sh ./

# update-rc.d boot_script.sh defaults 99

#### Finish

# rm /debian/usr/share/buendia/site/99-local
# reboot
