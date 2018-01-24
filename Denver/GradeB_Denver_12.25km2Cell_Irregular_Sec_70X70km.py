# Date: 22nd Nov 2016. 
import csv
from mpl_toolkits.basemap import Basemap 
import matplotlib.pyplot as plt 
import matplotlib.lines as mlines 
import numpy as np 
import pandas as pd
from matplotlib.patches import Polygon
import geopy
import json
from geopy.distance import VincentyDistance
from geopy.distance import vincenty
from matplotlib.path import Path
from numba import autojit
import itertools as IT

from datetime import datetime
startTime = datetime.now()

# Enter the lat long of location that is the center of the area. We choose an area of 20KmX20Km. lat_S and long_S
# are the latitude and longitude of the chosen city

Side_secon_net = 70
Side_of_cell = 3.5
diag_secon_net = ((Side_secon_net**2+ Side_secon_net**2)**0.5)/2
lat_S = 39.7392
long_S = -104.9903
d = [diag_secon_net]*4
dis = [400]*4
num_of_cells = (Side_secon_net**2)/(Side_of_cell**2)

# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
origin = geopy.Point(lat_S, long_S)

# With the north line across the city we find the bearing of the diagonal corners(lower left and upper right) of the square around 
# the city. Convert bearing from degrees to radians
bearing_deg = [45,135,225,315]
des = []
des_big = []
for index in range(len(bearing_deg)):
    destination = VincentyDistance(kilometers=d[index]).destination(origin,bearing_deg[index])
    destination_big = VincentyDistance(kilometers=dis[index]).destination(origin,bearing_deg[index])
    lat2 = destination.latitude
    lon2 = destination.longitude
    latBig = destination_big.latitude
    lonBig = destination_big.longitude
    val = [lat2,lon2]
    valBig = [latBig,lonBig]
    des.append(val)
    des_big.append(valBig)

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon are the lat/lon values of the lower left and upper right corners of the map.
# resolution = 'i'means use intermediate resolution coastlines.lon_0, lat_0 are the central longitude and latitude of 
# the projection.
m = Basemap(projection='merc',llcrnrlon=des[2][1], llcrnrlat=des[2][0],urcrnrlon=des[0][1],urcrnrlat=des[0][0],resolution='h',area_thresh = 0.1,            lat_0 = lat_S,lon_0 = long_S)
p1,p2 = m(long_S,lat_S)
m.plot(p1, p2, 'r^', markersize=6)
label = 'Denver'
plt.text(p1+1000, p2+500, label)
m.drawcoastlines(linewidth=1)
m.drawcountries(linewidth=1)
m.fillcontinents(color="#ffe4b5",lake_color="#afeeee")
m.drawmapboundary(fill_color="#afeeee")

# function to draw polygons
def draw_screen_poly( lats, lons, m):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='red', alpha=0.1 )
    plt.gca().add_patch(poly)


# Creating the strips of cells
Lat_A = des[3][0]
Lon_A = des[3][1]
Lat_B = des[0][0]
Lon_B = des[0][1]

origin = geopy.Point(Lat_A, Lon_A)
bearing_deg_A_to_B = 90
d_A_to_B = Side_of_cell
destination = VincentyDistance(kilometers=d_A_to_B).destination(origin,bearing_deg_A_to_B)
Lat_B = destination.latitude
Lon_B = destination.longitude

origin = geopy.Point(Lat_A, Lon_A)
bearing_deg_A_to_D = 180
d_A_to_D = Side_of_cell
destination = VincentyDistance(kilometers=d_A_to_D).destination(origin,bearing_deg_A_to_D)
Lat_D = destination.latitude
Lon_D = destination.longitude

origin = geopy.Point(Lat_B, Lon_B)
bearing_deg_B_to_C = 180
d_B_to_C = Side_of_cell
destination = VincentyDistance(kilometers=d_B_to_C).destination(origin,bearing_deg_B_to_C)
Lat_C = destination.latitude
Lon_C = destination.longitude

bearing_deg_rt = [45,45,90]
d_rt = [((2*(Side_of_cell**2))**0.5)/2,(2*(Side_of_cell**2))**0.5,Side_of_cell]
center = []
rt_D = []
rt_A = [[Lon_A,Lat_A]]
A = []
D = []

for strip in range(0,int(Side_secon_net/Side_of_cell)):
    origin = geopy.Point(Lat_A, Lon_A)
    bearing_deg_A_to_D = 180
    d_A_to_D = Side_of_cell
    destination = VincentyDistance(kilometers=d_A_to_D).destination(origin,bearing_deg_A_to_D)
    Lat_D = destination.latitude
    Lon_D = destination.longitude
    val_D = (Lon_D,Lat_D)
    rt_D.append(val_D)
    for i in range(0,int(Side_secon_net/Side_of_cell)):
        for j in range(0,len(bearing_deg_rt)):
            if j==0: 
                origin = geopy.Point(Lat_D, Lon_D)
                destination = VincentyDistance(kilometers=d_rt[j]).destination(origin,bearing_deg_rt[j])
                Lat_center = destination.latitude
                Lon_center = destination.longitude
                val_center = (Lon_center,Lat_center)
                center.append(val_center)
            elif j==1:
                origin = geopy.Point(Lat_D, Lon_D)
                destination = VincentyDistance(kilometers=d_rt[j]).destination(origin,bearing_deg_rt[j])
                Lat_rt_A = destination.latitude
                Lon_rt_A = destination.longitude
                val_A = (Lon_rt_A,Lat_rt_A)
                rt_A.append(val_A)
            elif j==2:
                origin = geopy.Point(Lat_D, Lon_D)
                destination = VincentyDistance(kilometers=d_rt[j]).destination(origin,bearing_deg_rt[j])
                Lat_rt_D = destination.latitude
                Lon_rt_D = destination.longitude
                val_D = (Lon_rt_D,Lat_rt_D)
                rt_D.append(val_D)
                Lat_D = Lat_rt_D
                Lon_D = Lon_rt_D
    origin = geopy.Point(Lat_A, Lon_A)
    bearing_deg_A_to_newA = 180
    d_A_to_newA = Side_of_cell
    destination = VincentyDistance(kilometers=d_A_to_newA).destination(origin,bearing_deg_A_to_newA)
    Lat_A = destination.latitude
    Lon_A = destination.longitude
    val_A = (Lon_A,Lat_A)
    rt_A.append(val_A)
    A.append(rt_A)
    D.append(rt_D)
    rt_A = [val_A]
    rt_D = []
    
for strip in range(0,int(Side_secon_net/Side_of_cell)): 
    for k in range(0,int(Side_secon_net/Side_of_cell)):
        Lat = [A[strip][k][1],D[strip][k][1],D[strip][k+1][1],A[strip][k+1][1]]
        Lon = [A[strip][k][0],D[strip][k][0],D[strip][k+1][0],A[strip][k+1][0]]
        draw_screen_poly(Lat,Lon,m)
    plt.title('Strip with %.1f km X %.1f km cells around Denver over %d KmX %d Km area' %(Side_of_cell,Side_of_cell,Side_secon_net,Side_secon_net))
    plt.savefig('Strip with %.1f km X %.1f km across Denver( %d Km X %d Km).png'%(Side_of_cell,Side_of_cell,Side_secon_net,Side_secon_net),dpi=300)
plt.show()

# function to check if the point is on the polygon
EPSILON = 2
def pointOnPolygon(point,poly):
    for i in range(len(poly)):
        [a, b] = poly[i-1], poly[i]
        if abs(vincenty(a,point,miles=False) + vincenty(b,point,miles=False) -vincenty(a,b,miles=False)) < EPSILON:
            return True
    return False
pointOnPolygon = autojit(pointOnPolygon)

# compute list of channels that are not available; chan_NA is the list of list of channels not available for the center node

df = pd.read_csv('Denver_Irregular_Ser_Cont_Points_GradeB.csv')
cols_to_use = df.columns
cols_to_use = []
for degree in range(1, 360, 2):
  cols_to_use.append("Latitude."+str(degree))
  cols_to_use.append("Longitude."+str(degree))
dfa  = df[cols_to_use]
fr = dfa
fr.values.shape
poly_overall = fr.values.reshape((len(dfa),180, 2))
path_overall = []
for row in range(0, len(dfa)):
    temp = dfa.ix[row]
    path_individual_row= [m(t[1], t[0]) for t in poly_overall[row]]    
    path_overall.append(Path(path_individual_row))
chan_NA = []
chan_NA_co =[]
chan_NA_adj = []
chan_NA_SET = []
Num_chan_avl = []
chan_avl = []
CELL_MAX= len(center)    #Total number of cells in the area
out_channels = {} 
for cell in range(0,CELL_MAX):
    CHAN_CNT_USE = []
    center_ext = []
    print 'Cell no is'
    print cell
    TV_loc = []
    TV_ERP = []
    TV_HAAT = []
    TV_app_id = []
    TV_fac_id = []
    center_lat_lon = (center[cell][1],center[cell][0])
    center_ext.append(center_lat_lon)
    chan_cnt_use_co = []
    chan_cnt_use_adj = []
    chan_cnt_use = []
    # compute more points to check if same channel is available all across the cell
    bear_degree = [45,135,225,315]
    dis = ((2*(Side_of_cell**2))**0.5)/2
    orig = geopy.Point(center[cell][1],center[cell][0])
    for b in range(0,len(bear_degree)):
        destination = VincentyDistance(kilometers=dis).destination(orig,bear_degree[b])
        lat = destination.latitude
        lon = destination.longitude
        ext = (lat,lon)
        center_ext.append(ext)        
    for index in range(0,len(center_ext)):              
        CENTER = (center_ext[index][0],center_ext[index][1])
        lat_center_cell, long_center_cell = CENTER
        center_cell_projected = m(long_center_cell, lat_center_cell)
        for row in range(0, len(dfa)):
            if row%100==0:
                print row
            #Now checking per row
            path_row = path_overall[row]
            channel_no = df.ix[row]['station_channel']
            ERP_Tower = df.ix[row]['effective_erp']
            HAAT_Tower = df.ix[row]['HAAT_m']
            APP_ID = df.ix[row]['app_id']
            Facility_ID = df.ix[row]['facility_id']
            TV_Lat_Lon = [df.ix[row]['Latitude'],df.ix[row]['Longitude']]
            flag = False
            condition_1 = path_row.contains_point(center_cell_projected)
            if condition_1:
                flag = True
            if not condition_1:
                pol = poly_overall[row].tolist()
                condition_2 = pointOnPolygon(CENTER,pol)
                if condition_2:
                    flag = True
            if flag:
                if channel_no<=20:
                    continue
                elif channel_no==21:
                    chan_cnt_use.append(channel_no)
                    chan_cnt_use.append(channel_no+1)
                    chan_cnt_use_co.append(channel_no)
                    chan_cnt_use_adj.append(channel_no+1)
                    TV_loc.append(TV_Lat_Lon)
                    TV_ERP.append(ERP_Tower)
                    TV_HAAT.append(HAAT_Tower)
                    TV_app_id.append(APP_ID)
                    TV_fac_id.append(Facility_ID)               
                elif channel_no>21 and channel_no<51:
                    chan_cnt_use.append(channel_no-1)
                    chan_cnt_use.append(channel_no)
                    chan_cnt_use.append(channel_no+1)
                    chan_cnt_use_co.append(channel_no)
                    chan_cnt_use_adj.append(channel_no-1)
                    chan_cnt_use_adj.append(channel_no+1)
                    TV_loc.append(TV_Lat_Lon)
                    TV_ERP.append(ERP_Tower)
                    TV_HAAT.append(HAAT_Tower)
                    TV_app_id.append(APP_ID)
                    TV_fac_id.append(Facility_ID)  
                elif channel_no==51:
                    chan_cnt_use.append(channel_no-1)
                    chan_cnt_use.append(channel_no)
                    chan_cnt_use_co.append(channel_no)
                    chan_cnt_use_adj.append(channel_no-1)
                    TV_loc.append(TV_Lat_Lon)
                    TV_ERP.append(ERP_Tower)
                    TV_HAAT.append(HAAT_Tower)
                    TV_app_id.append(APP_ID)
                    TV_fac_id.append(Facility_ID)  
                else:
                    continue
        CHAN_CNT_USE.append(list(set(chan_cnt_use)))
        # Take intersection of all the channels that cannot be used
    chan_cnt_use = list(set(CHAN_CNT_USE[0] + CHAN_CNT_USE[1] + CHAN_CNT_USE[2] + CHAN_CNT_USE[3] + CHAN_CNT_USE[4]))
    chan_NA_set = list(set(chan_cnt_use))
    chan_np = np.array(chan_NA_set)
    chan_np = chan_np.flatten()
    all_chans = np.arange(21, 52)
    Avl_chan = np.setdiff1d(all_chans, chan_np).tolist()
    Num_chan = 31 - len(chan_NA_set)
    chan_cnt_use = list(set(chan_cnt_use))
    chan_cnt_use_co = list(set(chan_cnt_use_co))
    chan_cnt_use_adj = list(set(chan_cnt_use_adj))
    out = {"location":center[cell],
       "num_chan_aval":Num_chan,
       "chan_not_available":str(chan_cnt_use),
       "TV_Tower_Location":str(TV_loc),
       "TV_Tower_HAAT":str(TV_HAAT),
       "TV_Tower_ERP":str(TV_ERP),
       "TV_Tower_app_id":str(TV_app_id),
       "TV_Tower_fac_id":str(TV_fac_id),
       "co_channel_NA":str(chan_cnt_use_co),
       "adj_channel_NA":str(chan_cnt_use_adj),
       "Available_channel":Avl_chan,
       "Origin_xy":des_big[2]}
    out_channels[cell] = out
json.dump(out_channels, open('GradeB_Denver_%.1fkm2Cell_Irregular_Sec70X70km2.json'%(Side_of_cell),'w'))           
print datetime.now() - startTime

