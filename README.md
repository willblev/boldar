# boldar
Boldar (Bolet Radar) A python script which scrapes weather records and tries to pinpoint the best area for mushroom hunting in Catalunya.

The python script will download .csv files from http://www.aemet.es/ to its current directory, and then it will parse them for information about precipitation, wind, temperature, etc. It uses this data to rank the best areas for mushroom hunting.

In the future we plan to add:
-static profiles for each location (altitude, forest types, soil types, etc.) to improve the predictive power of this model
-static mushroom profiles for each species, as they tend to grow best in different conditions and at different times
-output to google maps to show the top 10 places to hunt
