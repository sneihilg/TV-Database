# Code to generate reduced search space for channel availability
import csv
import numpy as np 
from geopy.distance import vincenty

# Enter the lat long of location that is the center of the area. 
# Lat Long of Columbus    
lat_S = 39.9612
long_S = -82.9988

DIS = 400       # radius of area around Columbus
j=0
fieldname = []
#Create a sub-csv for Columbus to reduce search space for channel availability
with open('Irregular_Ser_Cont_Points_Buffer_HAAT10m.csv', 'rb') as csvfile:
    with open('Columbus_Irregular_Ser_Cont_Points_GradeB_SepDis.csv', 'w') as csvoutput:
        next(csvfile)
        writer = csv.writer(csvoutput, lineterminator='\n')
        fieldnames = ["app_id","facility_id","Grade_A","Grade_B","effective_erp","HAAT_m","station_channel"]
        for ls in range(361):
            fieldnames.extend(["Latitude","Longitude"])
        writer.writerow(fieldnames)
        tv_reader = csv.reader(csvfile, delimiter=',')
        for row in tv_reader:
            print j
            Lat_Tower = row[7]
            Lon_Tower = row[8]
            if vincenty([lat_S,long_S],[Lat_Tower,Lon_Tower])<=DIS:          
                pol = []
                if row[2] in (None,""):
                    App_ID = ""
                    Facility_ID = ""
                    Rad_A = ""
                    Rad_B = ""
                    ERP_Tower = ""
                    HT_Tower = float(row[5])
                    Lat_Tower = float(row[7])
                    Lon_Tower = float(row[8])
                    Lat_list = row[9::2]
                    Lon_list = row[10::2]
                    for ls in range(360):
                        pol.extend([float(Lat_list[ls]),float(Lon_list[ls])])
                    chan = float(row[6])
                else:    
                    App_ID = float(row[0])
                    Facility_ID = float(row[1])
                    Rad_A = float(row[2])
                    Rad_B = float(row[3])
                    ERP_Tower = float(row[4])
                    HT_Tower = float(row[5])
                    Lat_Tower = float(row[7])
                    Lon_Tower = float(row[8])
                    Lat_list = row[9::2]
                    Lon_list = row[10::2]
                    for ls in range(360):
                        pol.extend([float(Lat_list[ls]),float(Lon_list[ls])])
                    chan = float(row[6])
                Data = [App_ID,Facility_ID,Rad_A,Rad_B,ERP_Tower,HT_Tower,chan,Lat_Tower,Lon_Tower]
                Data.extend(np.array(pol))
                writer.writerow(Data)
                j = j+1
            else:
                j = j+1
                continue

