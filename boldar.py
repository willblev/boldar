#!/usr/bin/env python
# -*- coding: cp1252 -*-

import os, time, sys, csv, urllib, itertools
from datetime import date, timedelta

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
		self.max_temp=max_temp
		self.min_temp=min_temp
		self.avg_temp=avg_temp
		self.gust_wind=gust_wind
		self.max_wind=max_wind
		self.prec_24h=prec_24h
		self.prec_0_6= prec_0_6
		self.prec_6_12= prec_6_12
		self.prec_12_18= prec_12_18
		self.prec_18_24= prec_18_24
		self.days_ago= days_ago	
	
	def gen_score(self):
		if float(self.avg_temp)==15:
			score=11
		else:
			score=10/(abs(float(self.avg_temp)-15))  #ideal temp of 15C, more points for staying close
		score+=float(self.prec_24h)            #points for quantity of rain + extra for constant rain
		if float(self.prec_0_6) > 0:   
			score+=1
		if float(self.prec_6_12) > 0:
			score+=1
		if float(self.prec_12_18) > 0:
			score+=1
		if float(self.prec_18_24) > 0:
			score+=1

		score+=15-float(self.max_wind.strip()[0] )/2  #wind over 15kph will dry out mushrooms
		
		if float(self.min_temp.strip()[0] ) < 4:   # fixed penalties for extreme weather
			score+=-30
		if float(self.max_temp.strip()[0] ) > 23:
			score+=-10
		if float(self.gust_wind.strip()[0]) > 35:
			score+=-5
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
for x in range(1,8):    
	 lastweek=today - timedelta(x)
	 filename="aemet_weather."+lastweek.strftime('%d.%m.%Y')+".csv"
	 last_week[x]=filename
	 if os.path.isfile(filename):
		 print "File %s already exists!"%(filename)
		 pass
	 else:
		 need_to_download[x]=filename
		 

for key, value in need_to_download.iteritems():  ###3. download any missing weather data files
	print "Downloading %s ..."%(value)
	download_csv(value,key)
	time.sleep(0.4)	#break between downloads to (hopefully) avoid pissing off the server
	
list_of_stations=[]                              ###4. parse .csv files from 4-7 days ago
print "Condsidering weather patterns from %s through %s" %((today - timedelta(7)).strftime('%d.%m.%Y'), (today - timedelta(4)).strftime('%d.%m.%Y'))
for x in range(4,8):  
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
	'Coll de Narg\xf3':'42.173822, 1.316197',
	'Corbera, Pic dAgulles':'41.385064, 2.173403',
	'El Soleràs':'41.413591, 0.68027',
	'Espolla':'42.390946, 3.000686',
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
	'La Vall de Bianya':'42.23009, 2.440639',
	'La Vall de Boi':'42.528216, 0.848452',
	'Les Planes dHostoles':'42.056386, 2.538365',
	'Lleida':'41.61759, 0.620015',
	'Llorac':'41.556803, 1.307315',
	'Ma\xe7anet de Cabrenys':'42.387334, 2.752456',
	'Manresa':'41.729283, 1.822515',
	'Martinet':'42.359836, 1.694902',
	'Moi\xe0':'41.809948, 2.097169',
	'Mollerussa':'41.628738, 0.894182',
	'Monistrol de Montserrat':'41.610778, 1.843416',
	'Os de Balaguer':'41.873344, 0.720617',
	'Planoles':'42.316176, 2.103915',
	'Pontons':'41.415008, 1.51663',
	'Porqueres':'42.120195, 2.746287',
	'Prat de Llu\xe7an\xe8s':'42.119271, 2.10182',
	'Rasquera':'41.001926, 0.598512',
	'Reus Aeropuerto':'41.146576, 1.165839',
	'Ripoll':'42.199459, 2.190762',
	'Sabadell Aeropuerto':'41.522163, 2.101317',
	'Santa Susana':'41.639993, 2.710321',
	'Sant Hilari':'41.817373, 2.520736',
	'Sant Jaume dEnveja':'40.705971, 0.727148',
	'Sant Juli\xe0  de Vilatorta':'41.924627, 2.321074',
	'Sant Pau de Seg\xfaries':'42.263044, 2.367172',
	'Talarn':'42.186158, 0.899997',
	'Tarragona':'41.118883, 1.244491',
	'Tàrrega':'41.64808, 1.140943',
	'Tona':'41.849645, 2.227397',
	'Torà':'41.81054, 1.403618',
	'Torre de Cabdella':'42.421899, 0.982963',
	'Tortosa':'40.812578, 0.521442',
	'Valls':'41.285445, 1.249459',
	'Vandell\xf3s':'41.019496, 0.831619',
	'Vilafranca del Pened\xe8s':'41.346127, 1.69794'


}


os.system("cat map_webpage_beginning.txt > map_w_scores.html") # adds the html and beginning of JS to new webpage
outfile=open("map_w_scores.html",'a')
for station in scores:
	if  scores[station]<= 10:
		pin_color='red'
	elif scores[station] >10 and scores[station] <= 75:
		pin_color='yellow'
	elif scores[station] >75:
		pin_color='green'	
	outfile.write("\t\t\t\t['%s', %s,'http://maps.google.com/mapfiles/ms/icons/%s-dot.png'],\n" % (station,station_location[station], pin_color))
outfile.close()

os.system("cat map_webpage_end.txt >> map_w_scores.html") # adds the html and beginning of JS to new webpage
os.system("x-www-browser map_w_scores.html")


