# Code to generate reduced search space for channel availability
import csv
import numpy as np 
from geopy.distance import vincenty

# Enter the lat long of location that is the center of the area. lat_S and long_S
# are the latitude and longitude of Columbus
    
lat_S = 39.9612
long_S = -82.9988

DIS = 400
j=0
fieldname = []
#Create a sub-csv for Columbus to reduce search space for channel availability
with open('TV_TOWER_DATA_FINAL.csv', 'rb') as csvfile:
    with open('Columbus_Irregular_Ser_Cont_Points_GradeB.csv', 'w') as csvoutput:
        next(csvfile)
        writer = csv.writer(csvoutput, lineterminator='\n')
        fieldnames = ["app_id","facility_id","Grade_A","Grade_B","effective_erp","HAAT_m","station_channel"]
        for ls in range(361):
            fieldnames.extend(["Latitude","Longitude"])
        writer.writerow(fieldnames)
        tv_reader = csv.reader(csvfile, delimiter=',')
        for row in tv_reader:
            print j
            Lat_Tower = row[18]
            Lon_Tower = row[19]
            if vincenty([lat_S,long_S],[Lat_Tower,Lon_Tower])<=DIS:          
                pol = []
                if row[16] in (None,""):
                    App_ID = ""
                    Facility_ID = ""
                    Rad_A = ""
                    Rad_B = ""
                    ERP_Tower = ""
                    HT_Tower = float(row[12])
                    Lat_Tower = float(row[18])
                    Lon_Tower = float(row[19])
                    Lat_list = row[20::2]
                    Lon_list = row[21::2]
                    for ls in range(360):
                        pol.extend([float(Lat_list[ls]),float(Lon_list[ls])])
                    chan = float(row[15])
                else:    
                    App_ID = float(row[0])
                    Facility_ID = float(row[2])
                    Rad_A = float(row[16])
                    Rad_B = float(row[17])
                    ERP_Tower = float(row[1])
                    HT_Tower = float(row[12])
                    Lat_Tower = float(row[18])
                    Lon_Tower = float(row[19])
                    Lat_list = row[20::2]
                    Lon_list = row[21::2]
                    for ls in range(360):
                        pol.extend([float(Lat_list[ls]),float(Lon_list[ls])])
                    chan = float(row[15])
                Data = [App_ID,Facility_ID,Rad_A,Rad_B,ERP_Tower,HT_Tower,chan,Lat_Tower,Lon_Tower]
                Data.extend(np.array(pol))
                writer.writerow(Data)
                j = j+1
            else:
                j = j+1
                continue

