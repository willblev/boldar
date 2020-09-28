# Boldar
Boldar (Bolet Radar) A python script which scrapes weather records and tries to pinpoint the best area for mushroom hunting in Catalunya.

The script will download .csv files from http://www.aemet.es/ to its current directory, and then it will parse them for information about precipitation, wind, temperature, etc. It uses this data to rank the best areas for mushroom hunting.

In the future I want to add:

- static profiles for each location (altitude, forest types, soil types, etc.) to improve the predictive power of this model
- static mushroom profiles for each species, as they tend to grow best in different conditions and at different times
- output to google maps to show the top 10 places to hunt
- update to python 3


## Usage

In your terminal, navigate to the directory containing all of Boldar's files, then run _boldar.py_ with python 2:
```
cd ~/Downloads/boldar-main/ && python2 boldar.py
```

It may raise an error the first time you run it, as the script was intended to be used with several weeks' worth of weather data, and the Aemet website will only permit you to automatically scrape data from the last week. The prediction is set to use weather data from the previous two weeks, so you should run it once or twice a week for a few weeks (to accumulate sufficient daily weather reports) before it will return useful predictions.
