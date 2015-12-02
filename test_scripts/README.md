### Test scripts

The scripts in the test_scripts folder are for development and debugging.

| File       | Function | Example |
| ---------- | ------ | ---------|
| `battery_rgb.py` `server_rgb.py` | Control the battery/server LED manually: 3 RGB arguments of 0/1 | `python battery_rgb.py 1 0 0` (activates red LED) |
| `flash_pin.py`  | Flash a particular pin by its `mraa` library number | `python flash_pin.py 32` |
| `leds_on.py` `leds_off.py` | Switch all LED's on and off | `python leds_on.py` |
| `report_leds.py` | Report on the current logic status of all GPIO pins | `python report_leds.py` |
| `test_battery_leds.py` `test_server_leds.py` | Flash the battery/server LEDs | `python test_battery_leds.py` |


#### console friendly version

+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+
| File                                         | Function                                                        | Example                                           |
+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+
| `battery_rgb.py` `server_rgb.py`             | Control the battery/server LED manually: 3 RGB arguments of 0/1 | `python battery_rgb.py 1 0 0` (activates red LED) |
+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+
| `flash_pin.py`                               | Flash a particular pin by its `mraa` library number             | `python flash_pin.py 32`                          |
+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+
| `leds_on.py` `leds_off.py`                   | Switch all LED's on and off                                     | `python leds_on.py`                               |
+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+
| `report_leds.py`                             | Report on the current logic status of all GPIO pins             | `python report_leds.py`                           |
+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+
| `test_battery_leds.py` `test_server_leds.py` | Flash the battery/server LEDs                                   | `python test_battery_leds.py`                     |
+----------------------------------------------+-----------------------------------------------------------------+---------------------------------------------------+