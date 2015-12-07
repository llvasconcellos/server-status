#### Edison Battery Analysis

This is a basic script that runs in R.  It calculates the average battery duration in hours based on the Edison's battery log data, and optionally returns a plot of the analysis - `analysis_plot.pdf`.


The script accepts a `csv` file (no header row) containing columns of numeric battery values as logged by the Edison in file `battery_charge_log.csv` on the SD card.  That data should be split manually into columns with each representing a full drain session on the battery (i.e. without any system down-time or recharging).  Save the new file as `battery_data.csv`

| drain 1<sup>*</sup> | drain 2 |
|----|----|
| 66 | 83 |
| 65 | 80 |
| 64 | 78 |
| 63 | 75 |
| 62 | 74 |
| 59 | 73 |
| 57 |    |
| 56 |    |

<sup>__*</sup> Header for illustration only - the csv should not have a header row.__

You can run the script manually in R or by bash command line by navigating to the folder and running `Rscript battery_life_analysis.R`.  If you want to graph the battery performances you'll need to make sure package `ggplot2` is installed and it's path is included in `.libPaths()`.

![](https://cdn.rawgit.com/geotheory/server-status/master/battery/battery_plot.png)
