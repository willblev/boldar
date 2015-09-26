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
			
				
		self.name= name
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
	
	def get_score(self):
		score=10/abs(float(self.avg_temp)-15)  #ideal temp of 15C, more points for staying close
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
for x in range(7,8):  
	parse_csv(last_week[x],x,list_of_stations)
	
	
list_of_stations.sort(key=lambda x: x.name, reverse=False) # arrange list by station name (secondary order by days ago)
scores={}
for station in list_of_stations:
	if station.name in scores:
		scores[station.name]+=station.get_score()
	else:
		scores[station.name]=station.get_score()

for w in sorted(scores, key=scores.get, reverse=True):
  print w, scores[w]
	

