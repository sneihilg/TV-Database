#Generate separation distance points (when it is irregular) around TV tower to use it to get an estimate of available channels.

import csv
from mpl_toolkits.basemap import Basemap 
import matplotlib.pyplot as plt 
import matplotlib.lines as mlines 
import numpy as np 
import pandas as pd
from matplotlib.patches import Polygon
import geopy
from geopy.distance import VincentyDistance
from geopy.distance import vincenty
import math

Rad_A = []              #Radius for Grade A service contour
Rad_B = []              #Radius for Grade B service contour
Lat_Tower = []          #Latitude of TV tower
Lon_Tower = []          #Longitude of TV tower
chan = []               #Channel 

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
        
Buffer_distance_10 = 11.1
j=0
#Create a csv for secondary antenna height 10 m and irregular Grade B service contour
with open('TV_TOWER_DATA.csv', 'rb') as csvfile:
    with open('Protected_Contour_Points.csv', 'w') as csvoutput:
        next(csvfile)
        writer = csv.writer(csvoutput, lineterminator='\n')
        tv_reader = csv.reader(csvfile, delimiter=',')
        for row in tv_reader:
            print j
            pol = []
            if row[16] in (None,""):
                App_ID = ""
                Facility_ID = ""
                Rad_A = ""
                Rad_B = ""
                ERP_Tower = ""
                HT_Tower = float(row[12])
                Lat_Tower = row[18]
                Lon_Tower = row[19]
                Lat_list = row[20::2]
                Lon_list = row[21::2]
                for ls in range(360):
                    pointA = (float(Lat_Tower),float(Lon_Tower))
                    pointB = (float(Lat_list[ls]),float(Lon_list[ls]))
                    origin = geopy.Point(float(Lat_list[ls]),float(Lon_list[ls]))
                    bearing = calculate_initial_compass_bearing(pointA, pointB)
                    destination = VincentyDistance(kilometers=Buffer_distance_10).destination(origin,bearing)
                    Lat = destination.latitude
                    Lon = destination.longitude
                    pol.extend((Lat,Lon))
                chan = float(row[15])
            else:    
                App_ID = float(row[0])
                Facility_ID = float(row[2])
                Rad_A = float(row[16])
                Rad_B = float(row[17])
                ERP_Tower = float(row[1])
                HT_Tower = float(row[12])
                Lat_Tower = row[18]
                Lon_Tower = row[19]
                Lat_list = row[20::2]
                Lon_list = row[21::2]
                for ls in range(360):
                    pointA = (float(Lat_Tower),float(Lon_Tower))
                    pointB = (float(Lat_list[ls]),float(Lon_list[ls]))
                    origin = geopy.Point(float(Lat_list[ls]),float(Lon_list[ls]))
                    bearing = calculate_initial_compass_bearing(pointA, pointB)
                    destination = VincentyDistance(kilometers=Buffer_distance_10).destination(origin,bearing)
                    Lat = destination.latitude
                    Lon = destination.longitude
                    pol.extend((Lat,Lon))
                chan = float(row[15])
            Data = [App_ID,Facility_ID,Rad_A,Rad_B,ERP_Tower,HT_Tower,chan,Lat_Tower,Lon_Tower]
            Data.extend(np.array(pol))
            writer.writerow(Data)
            j=j+1

#Buffer_distance_3 = 7.3
#k=0
##Read csv and get data. Note: csv row starts from row[0]
#with open('TV_TOWER_DATA_FINAL.csv', 'rb') as csvfile:
#    with open('Irregular_Ser_Cont_Points_Buffer_HAAT3m.csv', 'w') as csvoutput:
#        next(csvfile)
#        writer = csv.writer(csvoutput, lineterminator='\n')
#        tv_reader = csv.reader(csvfile, delimiter=',')
#        for row in tv_reader:
#            print k
#            pol = []
#            if row[16] in (None,""):
#                App_ID = ""
#                Facility_ID = ""
#                Rad_A = ""
#                Rad_B = ""
#                ERP_Tower = ""
#                HT_Tower = float(row[12])
#                Lat_Tower = row[18]
#                Lon_Tower = row[19]
#                Lat_list = row[20::2]
#                Lon_list = row[21::2]
#                for ls in range(360):
#                    origin = geopy.Point(float(Lat_list[ls]),float(Lon_list[ls]))
#                    bearing = 90
#                    destination = VincentyDistance(kilometers=Buffer_distance_3).destination(origin,bearing)
#                    Lat = destination.latitude
#                    Lon = destination.longitude
#                    pol.extend((Lat,Lon))
#                chan = float(row[15])
#            else:    
#                App_ID = float(row[0])
#                Facility_ID = float(row[2])
#                Rad_A = float(row[16])
#                Rad_B = float(row[17])
#                ERP_Tower = float(row[1])
#                HT_Tower = float(row[12])
#                Lat_Tower = row[18]
#                Lon_Tower = row[19]
#                Lat_list = row[20::2]
#                Lon_list = row[21::2]
#                for ls in range(360):
#                    origin = geopy.Point(float(Lat_list[ls]),float(Lon_list[ls]))
#                    bearing = 90
#                    destination = VincentyDistance(kilometers=Buffer_distance_3).destination(origin,bearing)
#                    Lat = destination.latitude
#                    Lon = destination.longitude
#                    pol.extend((Lat,Lon))
#                chan = float(row[15])
#            Data = [App_ID,Facility_ID,Rad_A,Rad_B,ERP_Tower,HT_Tower,chan,Lat_Tower,Lon_Tower]
#            Data.extend(np.array(pol))
#            writer.writerow(Data)
#            k=k+1
