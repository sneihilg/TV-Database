from mpl_toolkits.basemap import Basemap 
import matplotlib.pyplot as plt 
import pandas as pd
from matplotlib.patches import Polygon
import geopy
from geopy.distance import VincentyDistance
import json
import matplotlib.patches as mpatches

from datetime import datetime
startTime = datetime.now()

Side_secon_net = 70
Side_of_cell = 10
diag_secon_net = ((Side_secon_net**2+ Side_secon_net**2)**0.5)/2
lat_S = 39.96696 
long_S = -82.99244
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
m = Basemap(projection='merc',llcrnrlon=des_big[2][1], llcrnrlat=des_big[2][0],urcrnrlon=des_big[0][1],urcrnrlat=des_big[0][0],resolution='h',area_thresh = 0.1,lat_0 = lat_S,lon_0 = long_S)
p1,p2 = m(long_S,lat_S)
m.plot(p1, p2, 'r^', markersize=3)
label = 'Columbus'
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

Data = json.load(open('GrdB_Columbus_%dkm2_Sim_Data_Sec_70X70km2.json'%(Side_of_cell),'r'))

for cells in range(0,len(Data)):
    cell_coord = (Data[str(cells)]['cell_coord'])
    lat_cell_ver = []
    lon_cell_ver = []
    for ver in range(0,len(cell_coord)):
        lat_cell_ver.append(cell_coord[ver][0])
        lon_cell_ver.append(cell_coord[ver][1])
    draw_screen_poly(lat_cell_ver,lon_cell_ver,m)
    
df = pd.read_csv('Columbus_Irregular_Ser_Cont_Points_GradeB.csv')
cols_to_use = df.columns
cols_to_use = []
for degree in range(1, 360, 2):
  cols_to_use.append("Latitude."+str(degree))
  cols_to_use.append("Longitude."+str(degree))
dfa  = df[cols_to_use]
fr = dfa
fr.values.shape
poly_overall = fr.values.reshape((len(dfa),180, 2))

for cell in range(0,len(Data)):
    TV_tower = (Data[str(cell)]['TV_TX_Loc'])
    TV_rec = (Data[str(cell)]['TV_RX_Loc'])
    chan = (Data[str(cell)]['num_chan_aval'])
    channel = (Data[str(cell)]['chan_available'])
    for channels in range(0,chan):
        TV = TV_tower[channels]
        RX = TV_rec[channels]
        chann = channel[channels]
        for num_pri in range(0,len(TV)):
            TV_loc_lat = TV[num_pri][0]
            TV_loc_lon = TV[num_pri][1]
            RX_loc_lat = RX[num_pri][0]
            RX_loc_lon = RX[num_pri][1]
            Lats = []
            Lons = []
            for row in range(0,len(df)):
                TV_Tower_lat = df.ix[row]['Latitude']
                TV_Tower_lon = df.ix[row]['Longitude']
                channel_no = df.ix[row]['station_channel']
                if (TV_Tower_lat==TV_loc_lat) and (TV_Tower_lon==TV_loc_lon) and (chann==channel_no):
                   ser_cont = poly_overall[row]                   
                   Lat_tx = TV_loc_lat
                   Lon_tx = TV_loc_lon
                   x_t,y_t = m(Lon_tx,Lat_tx)
                   m.plot(x_t, y_t, 'k^', markersize=3) 
                   Lat_rx = RX_loc_lat
                   Lon_rx = RX_loc_lon
                   x_r,y_r = m(Lon_rx,Lat_rx)
                   m.plot(x_r, y_r, 'b^', markersize=3) 
                   for k in range (0,len(ser_cont)):
                       Lats.append(ser_cont[k][0])
                       Lons.append(ser_cont[k][1])
                   x,y = m(Lons, Lats) 
                   if chann==27:
                       m.plot(x, y, '-', linewidth=1, color='red',alpha=1) 
                   elif chann==28:
                       m.plot(x, y, '-', linewidth=1, color='blue',alpha=1)
                   elif chann==29:
                       m.plot(x, y, '-', linewidth=1, color='green',alpha=1)
                   elif chann==30:
                       m.plot(x, y, '-', linewidth=1, color='black',alpha=1)
                   elif chann==31:
                       m.plot(x, y, '-', linewidth=1, color='yellow',alpha=1)
                   elif chann==40:
                       m.plot(x, y, '-', linewidth=1, color='brown',alpha=1)    
                   elif chann==41:
                       m.plot(x, y, '-', linewidth=1, color='magenta',alpha=1)  
                   elif chann==41:
                       m.plot(x, y, '-', linewidth=1, color='orange',alpha=1)  
                   elif chann==43:
                       m.plot(x, y, '-', linewidth=1, color='pink',alpha=1)
                   elif chann==44:
                       m.plot(x, y, '-', linewidth=1, color='aqua',alpha=1)
                   elif chann==50:
                       m.plot(x, y, '-', linewidth=1, color='coral',alpha=1)
                   elif chann==51:
                       m.plot(x, y, '-', linewidth=1, color='lightgreen',alpha=1)
red = mpatches.Patch(color='red', label='27')
blue = mpatches.Patch(color='blue', label='28')
green = mpatches.Patch(color='green', label='29')
black = mpatches.Patch(color='black', label='30')
yellow = mpatches.Patch(color='yellow', label='31')
brown = mpatches.Patch(color='brown', label='40')
magenta = mpatches.Patch(color='magenta', label='41')
orange = mpatches.Patch(color='orange', label='42')
pink = mpatches.Patch(color='pink', label='43')
aqua = mpatches.Patch(color='aqua', label='44')
coral = mpatches.Patch(color='coral', label='50')
lightgreen = mpatches.Patch(color='lightgreen', label='51')
plt.legend(handles=[red,blue,green,black,yellow,brown,magenta,orange,pink,aqua,coral,lightgreen],title='Channel No.',bbox_to_anchor=(1., 0., 0.8 , 0), loc=3,ncol = 1, borderaxespad=0.2,fontsize=11)
plt.title('Map of TV towers with Irregular Service Contour')
plt.tight_layout()
plt.savefig('TV Tower and worst receiver Sec (70X70)km2.png',dpi=300,bbox_inches='tight')
plt.show()