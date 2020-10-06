# Boldar
Boldar (Bolet Radar) A python script which scrapes weather records and tries to pinpoint the best area for mushroom hunting in Catalunya. It then outputs the prediction as an [interactive map](http://willblev.github.io/boldar/EXAMPLE-map_w_scores.html). 

The script will download .csv files from http://www.aemet.es/ to its current directory, and then it will parse them for information about precipitation, wind, temperature, etc. It uses this data to rank the best areas for mushroom hunting.

## Example

After collecting weather data from dozens of locations around Catalunya, Boldar makes a prediction of how likely it is that mushrooms are growing in each area. It ranks them from best to worst and saves these values in a file called [_scores_predicted.txt_](http://willblev.github.io/boldar/EXAMPLE-scores_predicted.txt) that looks like this:

```
Sant Pau de Segúries, 941
Planoles, 687
Vall de Boí, 571
La Molina, 473
Tuixent, 356
Vilafranca del Penedes, 352
Sant Hilari, 331
```

Using these predictions, it creates an interactive map in a file called [_map_w_scores.html_](http://willblev.github.io/boldar/EXAMPLE-map_w_scores.html) with colored pins on each location; green pins signify that mushrooms are very likely to be growing in the area, yellow pins means that there are probably mushrooms around, and red pins mean you aren't likely to find any mushrooms at all: 

![Example of boldar prediction map](https://github.com/willblev/boldar/blob/main/map_w_scores.png?raw=true)

**Hovering your mouse over a pin will display the name and score of the location.**

## Usage

In your terminal, navigate to the directory containing all of Boldar's files, then run _boldar.py_ with python 2:
```
cd ~/Downloads/boldar-main/ && python2 boldar.py
```

It may raise an error like _IOError: [Errno 2] No such file or directory: 'aemet_weather.20.09.2020.csv'_ the first few times that you run it: This is because the default parameters include several weeks' worth of weather data, but the Aemet website will only permit you to automatically scrape data from the last week. Therefore you need to run Boldar once or twice a week for a few weeks to accumulate sufficient daily weather reports before it will return any useful predictions.


## Future features

In the future I would like to add:

- static profiles for each location (altitude, forest types, soil types, etc.) to improve the predictive power of this model
- static mushroom profiles for each species, as different types of mushrooms tend to grow best in different conditions and at different times of the year
- output to google maps to show the top 10 places to hunt
- update to python 3
- find API to scrape multiple weeks' worth of data at once
- parse doppler images with CV libraries to have higher resolution predictions
