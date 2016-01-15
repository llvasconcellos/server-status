DTC=dtc

all: ds3234-bitbang-rpi-overlay.dtb

ds3234-bitbang-rpi-overlay.dtb: ds3234-bitbang-rpi-overlay.dts
        $(DTC) -@ -I dts -O dtb -o ds3234-bitbang-rpi-overlay.dtb ds3234-bitbang-rpi-overlay.dts

install-ds3234-bitbang-rpi-overlay.dtb: ds3234-bitbang-rpi-overlay.dtb
        cp ds3234-bitbang-rpi-overlay.dtb /boot/overlays/

install: install-ds3234-bitbang-rpi-overlay.dtb

clean:
        rm *.dtb
