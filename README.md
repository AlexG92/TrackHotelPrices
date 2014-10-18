TrackHotelPrices
================

A python script that should run as a cron job and keep track of specific hotel prices and how they change.

## Collect.py

Should be run as a cron job. Data gets written to data.csv

In the `URLS` dictionary, for the values, put the URL of expedia hotels that you want to track.

##Bestdates.py

Grabs the hotel prices for the whole year and puts it into a csv file for graphing.

`START_DATE` - The first day of possible vacation.

`LENGTH_OF_STAY` - How many nights you want the vacation to be

`URL` - The expedia hotel link. Please note you need to add the start_date_formatted and end_date_formatted.
