# Boldar
Boldar (Bolet Radar) A python script which scrapes weather records and tries to pinpoint the best area for mushroom hunting in Catalunya.

The script will download .csv files from http://www.aemet.es/ to its current directory, and then it will parse them for information about precipitation, wind, temperature, etc. It uses this data to rank the best areas for mushroom hunting.

## Example

After collecting weather data from dozens of locations around Catalunya, Boldar creates a map with colored pins on each location to indicate the likelihood of finding mushrooms there. Green pins signify that mushrooms are very likely to be growing in the area, yellow pins means that there are probably mushrooms around, and red pins mean you aren't likely to find any mushrooms at all. 

![Example of boldar prediction map](https://github.com/willblev/boldar/blob/main/map_w_scores.png?raw=true)
_Hovering your mouse over a pin will display the name of the location._

## Usage

In your terminal, navigate to the directory containing all of Boldar's files, then run _boldar.py_ with python 2:
```
cd ~/Downloads/boldar-main/ && python2 boldar.py
```

It may raise an error the first time you run it, as the script was intended to be used with several weeks' worth of weather data, and the Aemet website will only permit you to automatically scrape data from the last week. The prediction is set to use weather data from the previous two weeks, so you should run it once or twice a week for a few weeks (to accumulate sufficient daily weather reports) before it will return useful predictions.


## Future features

In the future I would like to add:

- static profiles for each location (altitude, forest types, soil types, etc.) to improve the predictive power of this model
- static mushroom profiles for each species, as different types of mushrooms tend to grow best in different conditions and at different times of the year
- output to google maps to show the top 10 places to hunt
- update to python 3
