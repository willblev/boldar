#!/usr/bin/env/python2
# -*- coding: cp1252 -*-

import os, time, sys, csv, urllib, itertools, math, subprocess
from datetime import date, timedelta

nearest_day=3
farthest_day=21

############## define functions /classes / etc. #########################

def download_csv(filename,days_ago):
	"""Function which downloads the .csv file & names it with appropriate date
	Day has to be an integer between 1-7 (1=1 day ago, 2=2 days ago, 3=3 days ago, etc.)"""
	getfile = urllib.URLopener()
	fetch_URL="http://www.aemet.es/en/eltiempo/observacion/ultimosdatos_cataluna_resumenes-diarios-anteriores.csv?k=cat&datos=det&w=2&f=tmax&x=d0%s"%(8-days_ago)
	getfile.retrieve(fetch_URL, "temp_aemet_weather.csv") ### downloads file & gives it a temporary name
	with open("temp_aemet_weather.csv", 'r') as temp_file:
		file_date=''
		while file_date=='':
			for line in temp_file:
				if line.startswith('Date'): ### parsing date
					split=line.split()
					date_str=split[1].rstrip(',')+" "+split[2]+" "+split[3]+" "+split[4]
					file_date=time.strptime(date_str,"%A %d %B %Y")### capture date info from string
					date_str=time.strftime("%d.%m.%Y",file_date)   ### convert date to str for file name
	os.rename("temp_aemet_weather.csv", "aemet_weather."+date_str+".csv") ### rename file with correct date
					

class Station:
	def __init__(self, name, province, max_temp, min_temp, avg_temp, gust_wind, max_wind, prec_24h, prec_0_6, prec_6_12, prec_12_18, prec_18_24, days_ago):    
		attribute_list=[name, province, max_temp, min_temp, avg_temp, gust_wind, max_wind, prec_24h, prec_0_6, prec_6_12, prec_12_18, prec_18_24]
		for attribute in attribute_list:
			if attribute=='':
				raise ValueError("An attribute is absent from %s" %(attribute, self.__class__.__name__))	
			
				
		self.name= name.replace("'", '')
		self.province= province
		split_max_temp=max_temp.split()
		self.max_temp=split_max_temp[0]
		split_min_temp=min_temp.split()
		self.min_temp=split_min_temp[0]
		self.avg_temp=avg_temp
		split_gust_wind=gust_wind.split()
		self.gust_wind=split_gust_wind[0]
		split_max_wind=max_wind.split()
		self.max_wind=split_max_wind[0]
		self.prec_24h=prec_24h
		self.prec_0_6= prec_0_6
		self.prec_6_12= prec_6_12
		self.prec_12_18= prec_12_18
		self.prec_18_24= prec_18_24
		self.days_ago= days_ago	
	
	def gen_score(self):
		if float(self.avg_temp)==15: #ideal temp of 15C, more points for staying close
			score=11
		else:
			score=10/(abs(float(self.avg_temp)-15))  

		score+=float(self.prec_24h)     #points for quantity of rain + extra for constant rain
		if float(self.prec_0_6) > 0:   
			score+=1
		if float(self.prec_6_12) > 0:
			score+=1
		if float(self.prec_12_18) > 0:
			score+=1
		if float(self.prec_18_24) > 0:
			score+=1

		if float(self.max_wind) > 15:  # wind over 15kph will dry out mushrooms, subtract points  
			score+=float(self.max_wind)/2  

		if float(self.min_temp ) < 5:   # penalties for extreme weather
			score+=-70
		if float(self.max_temp ) > 23:
			score+=-10
		if float(self.gust_wind) > 45:
			score+=-10
		score=score*(self.days_ago/3)
		return score
	
		
		
def parse_csv(file_name,days_ago,object_list):
	"""This function takes a .csv file and adds the data to a Station object"""
	csv_file= open(file_name, "rb")
	reader = csv.reader(csv_file)
	for line in itertools.islice(reader, 6, None):
		try:
			object_list.append(Station(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],days_ago))
		except:
			pass
	csv_file.close()



#############################################################  running script #######      
#1. Check the date
#2. Check dir to see if necessary files are there
#3. Download missing files and name appropriately
#4. Parse files and create Station objects
#5. Calculate scores for each Station, return sorted list of Stations + scores.
#6. Plot best locations on map using Google maps API

today=date.today()                                ###1. check today's date

last_week={}                                      ###2. check if necessary files are already downloaded
need_to_download={}
for x in range(1,7):    
	 lastweek=today - timedelta(x)
	 filename="aemet_weather."+lastweek.strftime('%d.%m.%Y')+".csv"
	 last_week[x]=filename
	 if os.path.isfile(filename):
		 print("File %s already exists!"%(filename))
		 pass
	 else:
		 need_to_download[x]=filename
		 

for key, value in need_to_download.items():  ###3. download any missing weather data files
	print("Downloading %s ..."%(value))
	download_csv(value,key)
	time.sleep(0.4)	#break between downloads to (hopefully) avoid pissing off the server
	
list_of_stations=[]                              ###4. parse .csv files from 4-7 days ago
print("Condsidering weather patterns from %s through %s" %((today - timedelta(farthest_day-1)).strftime('%d.%m.%Y'), (today - timedelta(nearest_day-1)).strftime('%d.%m.%Y')))
for x in range(nearest_day,farthest_day):
	try:
		parse_csv(last_week[x],x,list_of_stations)
	except KeyError:	# if we are looking farther back than 7 days, we have to add some keys to the dictionary 
		lastweek=today - timedelta(x)
		filename="aemet_weather."+lastweek.strftime('%d.%m.%Y')+".csv"
		last_week[x]=filename 
		parse_csv(last_week[x],x,list_of_stations)
	
	
list_of_stations.sort(key=lambda x: x.name, reverse=False) # arrange list by station name (secondary order by days ago)
scores={}
for station in list_of_stations:
	if station.name in scores:  
		scores[station.name]+=station.gen_score() ###5. generate simple scores for each station
	else:
		scores[station.name]=station.gen_score()

outfile=open("scores_predicted.txt",'w')
for w in sorted(scores, key=scores.get, reverse=True):  # save record of the scores
  outfile.write("%s, %d\n" %( w, scores[w]))
  print("%s, %d" %( w, scores[w]))
outfile.close()



### makes a map file with color coded points

station_location={
	'Alforja':'41.210753, 0.975144',
	'Arenys de Mar':'41.579707, 2.550868',
	'Artesa de Segre':'41.89566, 1.047242',
	'Balsareny':'41.863456, 1.874522',
	'Barcelona':'41.385064, 2.173403',
	'Barcelona, Museo Mar\xedtimo':'41.437544, 2.195073',
	'Barcelona Aeropuerto':'41.297445, 2.083294',
	'Berga':'42.10126, 1.843922',
	'Blanes':'41.675995, 2.790229',
	'Boss\xf2st':'42.785504, 0.692133',
	'Cabac\xe9s':'41.24746, 0.733977',
	'Caldes de Montbui':'41.631658, 2.166871',
	'Castell, Platja dAro':'41.814447, 3.032187',
	'Castell\xf3 dEmp\xfaries':'42.2583, 3.0750',
	'Coll de Narg\xf3':'42.173822, 1.316197',
	'Corbera, Pic dAgulles':'41.385064, 2.173403',
	'El Soleràs':'41.413591, 0.68027',
	'Espolla':'42.390946, 3.000686',
	'Estaci\xf3n de Tortosa (Roquetes)':'40.8209, 0.5021',
	'Esterri d\xc0neu':'42.626923, 1.122711',
	'Figueres':'42.265507, 2.958105',
	'Fogars de Montclús':'41.727493, 2.442842',
	'Girona':'41.979401, 2.821426',
	'Girona Aeropuerto':'41.905727, 2.76335',
	'Igualada':'41.584782, 1.622654',
	'Illes de Cerdanya,Cap de Rec':'41.61759, 0.620015',
	'Josa i Tuix\xe9n':'42.254595, 1.608097',
	'LEstartit':'42.051283, 3.190519',
	'La Molina':'42.337605, 1.934988',
	'La Pobla de Cérvoles':'41.366967, 0.915552',
	'La Pobla de Massaluca':'41.18078, 0.353361',
	'La Seo dUrgell':'42.357578, 1.455553',
	'La Seu dUrgell':'42.357578, 1.455553',
	'La Vall de Bianya':'42.23009, 2.440639',
	'La Vall de Boi':'42.528216, 0.848452',
	'Les Planes dHostoles':'42.056386, 2.538365',
	'Lleida':'41.61759, 0.620015',
	'Llimiana':'42.0667, 0.9167',
	'Llorac':'41.556803, 1.307315',
	'Ma\xe7anet de Cabrenys':'42.387334, 2.752456',
	'Manresa':'41.729283, 1.822515',
	'Martinet':'42.359836, 1.694902',
	'Moi\xe0':'41.809948, 2.097169',
	'Mollerussa':'41.628738, 0.894182',
	'Monistrol de Montserrat':'41.610778, 1.843416',
	'Naut Aran, Arties':'42.6988, 0.8717',
	'Os de Balaguer':'41.873344, 0.720617',
	'Planoles':'42.316176, 2.103915',
	'Pontons':'41.415008, 1.51663',
	'Porqueres':'42.120195, 2.746287',
	'Prat de Llu\xe7an\xe8s':'42.0071, 2.0310',
	'Prats de Llu\xe7an\xe8s':'42.0071, 2.0310',
	'Rasquera':'41.001926, 0.598512',
	'Reus Aeropuerto':'41.146576, 1.165839',
	'Ripoll':'42.199459, 2.190762',
	'Sabadell Aeropuerto':'41.522163, 2.101317',
	'Santa Susana':'41.639993, 2.710321',
	'Santa Susanna':'41.639993, 2.710321',
	'Sant Hilari':'41.817373, 2.520736',
	'Sant Jaume dEnveja':'40.705971, 0.727148',
	'Sant Juli\xe0  de Vilatorta':'41.924627, 2.321074',
	'Sant Pau de Seg\xfaries':'42.263044, 2.367172',
	'Sitges':'41.2372, 1.8059',
	'Talarn':'42.186158, 0.899997',
	'Tarragona':'41.118883, 1.244491',
	'T\xe0rrega':'41.64808, 1.140943',
	'Tona':'41.849645, 2.227397',
	'Torà':'41.81054, 1.403618',
	'Tordera - Granyanella':'41.4045, 1.1322',
	'Torre de Cabdella':'42.421899, 0.982963',
	'Tortosa':'40.812578, 0.521442',
	'Tuixent':'42.2316, 1.5663',
	'Valls':'41.285445, 1.249459',
	'Vall de Bo\xed':'42.5282, 0.8485',
	'Vandell\xf2s':'41.019496, 0.831619',
	'Vilafranca del Pened\xe8s':'41.346127, 1.69794',
	'Vilassar de Dalt':'41.5189, 2.3606'
}

# Calculate some statistics to describe the distribution of scores in order to color the pins

def variance(data, ddof=0):
	n = len(data)
	mean = sum(data) / n
	return sum((x - mean) ** 2 for x in data) / (n - ddof)

def stdev(data):
	var = variance(data)
	std_dev = math.sqrt(var)
	return std_dev

maximum_score=max(scores.values())
minimum_score=min(scores.values())
st_dev=stdev(scores.values())
mean=sum(scores.values())/len(scores.values())

low_score=mean-(.675*st_dev)  # below 1st quartile -> red
mid_score=mean                # 1st to 2nd quartile -> orange
high_score=mean+(.675*st_dev) # 2nd to 3rd quartile -> yellow
                              # 3rd to 4th quartile -> green

os.system("cat map_webpage_beginning.txt > map_w_scores.html") # adds the html and beginning of JS to new webpage
outfile=open("map_w_scores.html",'a')
for station in scores:
	if  scores[station]<= low_score:
		pin_color='red'
	elif scores[station] > low_score and scores[station] <= mid_score:
		pin_color='orange'
	elif scores[station] > mid_score and scores[station] <= high_score:
		pin_color='yellow'
	elif scores[station] > high_score:
		pin_color='green'	
	outfile.write("\t\t\t\t['%s : %s', %s,'http://maps.google.com/mapfiles/ms/icons/%s-dot.png'],\n" % (station,int(scores[station]),station_location[station], pin_color))

## add legend pins in bottom right corner to indicate scoring cutoffs
legend_lat=40.800008
legend_long=2.083294

outfile.write("\t\t\t\t['Low score cutoff (%s pins): x < %s', %s, %s,'http://maps.google.com/mapfiles/ms/icons/%s-dot.png'],\n" %("red", int(low_score),legend_lat, legend_long, "red"))

outfile.write("\t\t\t\t['Mid-low score cutoff (%s pins): %s < x < %s', %s, %s,'http://maps.google.com/mapfiles/ms/icons/%s-dot.png'],\n" %("orange", int(low_score), int(mid_score),legend_lat, legend_long+0.2, "orange"))

outfile.write("\t\t\t\t['Mid-high score cutoff (%s pins): %s < x < %s', %s, %s,'http://maps.google.com/mapfiles/ms/icons/%s-dot.png'],\n" %("yellow", int(mid_score), int(high_score),legend_lat, legend_long+0.4, "yellow"))

outfile.write("\t\t\t\t['High score cutoff (%s pins): %s < x', %s, %s,'http://maps.google.com/mapfiles/ms/icons/%s-dot.png'],\n" %("green", int(high_score),legend_lat, legend_long+0.6, "green"))

outfile.close()

os.system("cat map_webpage_end.txt >> map_w_scores.html") # adds the html and beginning of JS to new webpage

## Open browser with the map, then exit
subprocess.call("x-www-browser map_w_scores.html", shell=True)   #opens html document immediately; works on ubuntu
sys.exit()
