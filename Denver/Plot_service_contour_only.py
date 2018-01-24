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
    
color_palette = ('#0048BA','#B0BF1A','#AF002A','#84DE02','#9F2B68','#00C4B0','#FFBF00','#9966CC','#008000','#00FFFF',
                 '#568203','#FF2052','#FF9966','#FF91AF','#BFFF00','#006A4E','#66FF00','#08E8DE','#CC5500','#ED9121',
                 '#703642','#954535','#9FA91F','#6495ED','#00FFFF','#E1A95F','#F400A1','#8806CE','#A67B5B','#44D7A8','#50C878')

Side_secon_net = 70
Side_of_cell = 5
diag_secon_net = ((Side_secon_net**2+ Side_secon_net**2)**0.5)/2
lat_S = 39.7392
long_S = -104.9903
d = [diag_secon_net]*4
dis = [200]*4
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
m = Basemap(projection='merc',llcrnrlon=des_big[2][1], llcrnrlat=des_big[2][0],urcrnrlon=des_big[0][1],urcrnrlat=des_big[0][0],resolution='f',area_thresh = 0.1,lat_0 = lat_S,lon_0 = long_S,epsg = 4269)
m.arcgisimage(service='World_Topo_Map',xpixels=1200, verbose=True, zorder=1)
p1,p2 = m(long_S,lat_S)
m.plot(p1, p2, 'r*', markersize=10)
#label = 'Denver'
#plt.text(p1+1000, p2+500, label)
#m.drawcoastlines(linewidth=1.5)
#m.drawcountries(linewidth=1.5)
#m.fillcontinents(color="#ffe4b5",lake_color="#afeeee")
#m.drawmapboundary(fill_color="#afeeee")

# function to draw polygons
def draw_screen_poly( lats, lons, m):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='red', alpha=0.1 )
    plt.gca().add_patch(poly)

Data = json.load(open('GrdB_Denver_%dkm2_Sim_Data_Sec_70X70km2.json'%(Side_of_cell),'r'))

for cells in range(0,len(Data)):
    cell_coord = (Data[str(cells)]['cell_coord'])
    lat_cell_ver = []
    lon_cell_ver = []
    for ver in range(0,len(cell_coord)):
        lat_cell_ver.append(cell_coord[ver][0])
        lon_cell_ver.append(cell_coord[ver][1])
    draw_screen_poly(lat_cell_ver,lon_cell_ver,m)
    
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

chan_cell = []
for cell in range(0,len(Data)):
    TV_tower = (Data[str(cell)]['TV_TX_Loc'])
    TV_rec = (Data[str(cell)]['TV_RX_Loc'])
    chan = (Data[str(cell)]['num_chan_aval'])
    channel = (Data[str(cell)]['chan_available'])
    chan_cell.extend(channel)
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
                   m.plot(x_t, y_t, 'k^', markersize=10) 
                   Lat_rx = RX_loc_lat
                   Lon_rx = RX_loc_lon
                   x_r,y_r = m(Lon_rx,Lat_rx)
                   m.plot(x_r, y_r, 'bs', markersize=6) 
                   for k in range (0,len(ser_cont)):
                       Lats.append(ser_cont[k][0])
                       Lons.append(ser_cont[k][1])
                   x,y = m(Lons, Lats) 
                   if chann==21:
                       m.plot(x, y, '-', linewidth=1.5, color= color_palette[0],alpha=1) 
                   elif chann==22:
                       m.plot(x, y, '-', linewidth=1.5, color= color_palette[1],alpha=1)
                   elif chann==23:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[2],alpha=1)
                   elif chann==24:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[3],alpha=1)
                   elif chann==25:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[4],alpha=1)
                   elif chann==26:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[5],alpha=1)
                   elif chann==27:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[6],alpha=1)
                   elif chann==28:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[7],alpha=1)
                   elif chann==29:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[8],alpha=1)
                   elif chann==30:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[9],alpha=1)
                   elif chann==31:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[10],alpha=1)
                   elif chann==32:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[11],alpha=1)
                   elif chann==33:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[12],alpha=1)
                   elif chann==34:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[13],alpha=1)
                   elif chann==35:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[14],alpha=1)
                   elif chann==36:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[15],alpha=1)
                   elif chann==37:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[16],alpha=1)
                   elif chann==38:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[17],alpha=1)
                   elif chann==39:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[18],alpha=1)
                   elif chann==40:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[19],alpha=1)
                   elif chann==41:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[20],alpha=1)
                   elif chann==42:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[21],alpha=1)
                   elif chann==43:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[22],alpha=1)
                   elif chann==44:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[23],alpha=1)
                   elif chann==45:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[24],alpha=1)
                   elif chann==46:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[25],alpha=1)
                   elif chann==47:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[26],alpha=1)
                   elif chann==48:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[27],alpha=1)    
                   elif chann==49:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[28],alpha=1)  
                   elif chann==50:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[29],alpha=1)  
                   elif chann==51:
                       m.plot(x, y, '-', linewidth=1.5, color=color_palette[30],alpha=1)

chan_cell = sorted(list(set(chan_cell)))
handles = []
for k in range(0,len(chan_cell)):
    if chan_cell[k]==21:
        C_0 = mpatches.Patch(color=color_palette[0], label='21')
        handles.append(C_0)
    elif chan_cell[k]==22:
        C_1 = mpatches.Patch(color=color_palette[1], label='22')
        handles.append(C_1)
    elif chan_cell[k]==23:
        C_2 = mpatches.Patch(color=color_palette[2], label='23')
        handles.append(C_2)
    elif chan_cell[k]==24:
        C_3 = mpatches.Patch(color=color_palette[3], label='24')
        handles.append(C_3)
    elif chan_cell[k]==25:
        C_4 = mpatches.Patch(color=color_palette[4], label='25')
        handles.append(C_4)
    elif chan_cell[k]==26:
        C_5 = mpatches.Patch(color=color_palette[5], label='26')
        handles.append(C_5)
    elif chan_cell[k]==27:
        C_6 = mpatches.Patch(color=color_palette[6], label='27')
        handles.append(C_6)
    elif chan_cell[k]==28:
        C_7 = mpatches.Patch(color=color_palette[7], label='28')
        handles.append(C_7)
    elif chan_cell[k]==29:
        C_8 = mpatches.Patch(color=color_palette[8], label='29')
        handles.append(C_8)
    elif chan_cell[k]==30:
        C_9 = mpatches.Patch(color=color_palette[9], label='30')
        handles.append(C_9)
    elif chan_cell[k]==31:
        C_10 = mpatches.Patch(color=color_palette[10], label='31')
        handles.append(C_10)
    elif chan_cell[k]==32:
        C_11 = mpatches.Patch(color=color_palette[11], label='32')
        handles.append(C_11)
    elif chan_cell[k]==33:
        C_12 = mpatches.Patch(color=color_palette[12], label='33')
        handles.append(C_12)
    elif chan_cell[k]==34:
        C_13 = mpatches.Patch(color=color_palette[13], label='34')
        handles.append(C_13)
    elif chan_cell[k]==35:
        C_14 = mpatches.Patch(color=color_palette[14], label='35')
        handles.append(C_14)
    elif chan_cell[k]==36:
        C_15 = mpatches.Patch(color=color_palette[15], label='36')
        handles.append(C_15)
    elif chan_cell[k]==37:
        C_16 = mpatches.Patch(color=color_palette[16], label='37')
        handles.append(C_16)
    elif chan_cell[k]==38:
        C_17 = mpatches.Patch(color=color_palette[17], label='38')
        handles.append(C_17)
    elif chan_cell[k]==39:
        C_18 = mpatches.Patch(color=color_palette[18], label='39')
        handles.append(C_18)
    elif chan_cell[k]==40:
        C_19 = mpatches.Patch(color=color_palette[19], label='40')
        handles.append(C_19)
    elif chan_cell[k]==41:
        C_20 = mpatches.Patch(color=color_palette[20], label='41')
        handles.append(C_20)
    elif chan_cell[k]==42:
        C_21 = mpatches.Patch(color=color_palette[21], label='42')
        handles.append(C_21)
    elif chan_cell[k]==43:
        C_22 = mpatches.Patch(color=color_palette[22], label='43')
        handles.append(C_22)
    elif chan_cell[k]==44:
        C_23 = mpatches.Patch(color=color_palette[23], label='44')
        handles.append(C_23)
    elif chan_cell[k]==45:
        C_24 = mpatches.Patch(color=color_palette[24], label='45')
        handles.append(C_24)
    elif chan_cell[k]==46:
        C_25 = mpatches.Patch(color=color_palette[25], label='46')
        handles.append(C_25)
    elif chan_cell[k]==47:
        C_26 = mpatches.Patch(color=color_palette[26], label='47')
        handles.append(C_26)
    elif chan_cell[k]==48:
        C_27 = mpatches.Patch(color=color_palette[27], label='48')
        handles.append(C_27)
    elif chan_cell[k]==49:
        C_28 = mpatches.Patch(color=color_palette[28], label='49')
        handles.append(C_28)
    elif chan_cell[k]==50:
        C_29 = mpatches.Patch(color=color_palette[29], label='50')
        handles.append(C_29)
    elif chan_cell[k]==51:
        C_30 = mpatches.Patch(color=color_palette[30], label='51')
        handles.append(C_30)
if len(chan_cell)<=14:
    num_col = 1
elif (len(chan_cell)>14) and (len(chan_cell)<=28):
    num_col = 2
elif len(chan_cell)>28:
    num_col = 3
plt.legend(handles=list(handles),title='Channel No.',bbox_to_anchor=(1., 0., 0.8 , 0), loc=3,ncol = num_col, borderaxespad=0.2,fontsize=12)
#plt.title('Map of TV towers and White-Fi network (Denver)')
plt.tight_layout()
plt.savefig('TV Tower and Worst case receivers(70X70)km2.png',dpi=300,bbox_inches='tight')
plt.show()
print datetime.now() - startTime