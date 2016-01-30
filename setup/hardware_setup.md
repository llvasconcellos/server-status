## Hardware setup instructions


#### Edison platform purchase list

Except for the LiPo Fuel Gauge, this list is in the order that the blocks are mounted together.

| Item                     | Cost   | Image | Link  |
| ------------------------ | ------ | ----- | ----- |
| Intel Edison             | $49.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/intel_edison.jpg)        | [Sparkfun](https://www.sparkfun.com/products/13024) |
| Sparkfun Base Block      | $32.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_base.jpg)       | [Sparkfun](https://www.sparkfun.com/products/13045) |
| Sparkfun microSD Block   | $19.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_microsd.jpg)    | [Sparkfun](https://www.sparkfun.com/products/13041) |
| Sparkfun I2C Block       | $14.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_i2c.jpg)        | [Sparkfun](https://www.sparkfun.com/products/13034) |
| Sparkfun GPIO Block      | $14.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_gpio.jpg)       | [Sparkfun](https://www.sparkfun.com/products/13038) |
| Sparkfun Battery Block   | $24.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_battery.jpg)    | [Sparkfun](https://www.sparkfun.com/products/13037) |
| Sparkfun 2000maH battery | $12.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_2000mah.jpg)    | [Sparkfun](https://www.sparkfun.com/products/8483)  |
| Sparkfun LiPo Fuel Gauge |  $9.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_fuel_gauge.jpg) | [Sparkfun](https://www.sparkfun.com/products/10617) |
| Sparkfun Hardware Pack   |  $2.95 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/sparkfun_hardware_pack.jpg) | [Sparkfun](https://www.sparkfun.com/products/13187) |
| TOTAL                    | $183.55 | | |


#### Assembly

The units just click together.  Use the hardware pack to add structural protection.  Don't attach the Battery Block yet.

The 400 mAh battery mounted to the Battery Block should be replaced by male header pins.  Carefully peel the battery from the block.  Then touch the soldered connections with a hot soldering iron while gently pulling the battery and it will come away when the solder melts.  It helps to use a clamp at this point.  Then take a right-angled header strip and snap off a 2 pin length, then solder it in place so the pins point sideways away from the block.  Once the pins are in place the Battery Block can be snapped to the Sparkfun stack, and the last hardware screws added.

Next, straight header pins should be soldered to the connector holes on the GPIO Block.  To save space in the box we only put pins on the first 5 holes that we're using.

Likewise straight header pins should be soldered to the connector holes on the LiPo Fuel Gauge.

Now you're ready to start connecting jumper leads and testing your circuits with breadboard.


------------------------------

#### Hardware purchase list

The following can be sourced online or from any decent electronics store.

| Item | Specs | Image | Links |
| ---- | ----- | ----- | ----- |
| project box | ABS plastic, 130 x 68 x 46mm | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/project_box.jpg) | [MaplinUK](http://www.maplin.co.uk/p/abs-plastic-box-h2853-black-130x68x46mm-bz73q) |
| cable gland | PG11 / PG13.5 | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/cable_gland.jpg) | [MaplinUK](http://www.maplin.co.uk/p/ce-tek-ip68-polyamide-gland-pg11-up97f) |
| 3 x USB adaptor cable | Micro (male) to USB (female); min 15cm long | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/usb_adaptor_cable.png) | [AmazonUK](http://www.amazon.co.uk/gp/product/B00YOX4JU6?psc=1) |
| GPIO header | male, modifiable to 5 pin lengths | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/gpio_header.jpg) | ----- |
| 2 x LED bevel | fitting for 5mm LEDs | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/led_bevel.jpg) |  |
| jumper wires | 10cm long; female>female & female>male | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/jumper_wires.jpg) | [AmazonUK](http://www.amazon.co.uk/gp/product/B00UXNFIHE) [Sparkfun](https://www.sparkfun.com/products/9194) |
| 2 x 3.3k Ohm resistor | 4_band: ora/ora/red/gold 5_band: ora/ora/blck/brn/gld | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/resistor_3.3k.jpg) | [MaplinUK](http://www.maplin.co.uk/p/metal-film-06w-33k-ohm-resistor-m3k3) |
| 4 x 1.8k Ohm resistor | 4_band: brn/gre/red/gold 5_band: brn/gre/blck/brn/gld | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/resistor_1.8k.jpg) | [MaplinUK](http://www.maplin.co.uk/p/metal-film-06w-18k-ohm-resistor-m1k8) |
| heat-shrink tube | 1.5mm / 2.5mm thickness | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/heat_shrink_tube.jpg) | [MaplinUK](http://www.maplin.co.uk/p/15mm-heat-shrinkable-sleeving-1m-bf86t) |
| velcro tape | | ![](https://cdn.rawgit.com/geotheory/server-status/master/setup/img/velcro_tape.jpg) | [MaplinUK](http://www.maplin.co.uk/p/adhesive-60cm-hook-and-loop-black-n22gn) |





