from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt 
import pandas as pd
from matplotlib.patches import Ellipse, Polygon
import geopy
from geopy.distance import VincentyDistance
import json
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import ticker

from datetime import datetime
startTime = datetime.now()
    
Side_secon_net = 70
Side_of_cell = 3.5
diag_secon_net = ((Side_secon_net**2+ Side_secon_net**2)**0.5)/2
lat_S = 39.7392
long_S = -104.9903
d = [diag_secon_net]*4
dis = [70]*4
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
m.plot(p1, p2, 'r*', markersize=15)
plt.annotate('Denver', (p1,p2), xytext=(5, 5), textcoords='offset points',fontsize=20,weight = 'bold')

lat_cell_vertex = []
lon_cell_vertex = []
# function to draw polygons
def draw_screen_poly( lats, lons, m):
    x, y = m(lons,lats)
    lat_cell_vertex.append(y)
    lon_cell_vertex.append(x)
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='none', edgecolor = 'red', alpha=1,linewidth = 2)
    plt.gca().add_patch(poly)

Data = json.load(open('GrdB_Denver_%.1fkm2_Sim_Data_Sec_70X70km2.json'%(Side_of_cell),'r'))

chan_avl_cell = []
lat_center = []
lon_center = []
for cells in range(0,len(Data)):
    cell_coord = (Data[str(cells)]['cell_coord'])
    cell_center = (Data[str(cells)]['cell_center'])
    lat_center.append(cell_center[0])
    lon_center.append(cell_center[1])
    chan_avl_cell.append(Data[str(cells)]['num_chan_aval'])
    lat_cell_ver = []
    lon_cell_ver = []
    for ver in range(0,len(cell_coord)):
        lat_cell_ver.append(cell_coord[ver][0])
        lon_cell_ver.append(cell_coord[ver][1])

# heatmap
dim = int((num_of_cells)**(0.5))
lon_data = np.reshape(lon_center,(dim,dim))
lon_data = lon_data[1,:]
lat_data = np.reshape(lat_center,(dim,dim))
lat_data = lat_data[:,1]

# adding an extra row and column for pcolormesh
origin_lat = geopy.Point(lat_data[len(lat_data)-1],lon_data[0])
origin_lon = geopy.Point(lat_data[len(lat_data)-1],lon_data[len(lon_data)-1])
destination_lat = VincentyDistance(kilometers=Side_of_cell).destination(origin_lat,180)
destination_lon = VincentyDistance(kilometers=Side_of_cell).destination(origin_lon,90)
lat_data = np.append(lat_data,destination_lat.latitude)
lon_data = np.append(lon_data,destination_lon.longitude)

#shifting all lat/lon pairs by Side_of_cell/2
lat_data_new = []
for v in range(0,len(lat_data)):
    origin = geopy.Point(lat_data[v],lon_data[1])
    destination = VincentyDistance(kilometers=Side_of_cell/2).destination(origin,0)
    lat_data_new.append(destination.latitude)
    
lon_data_new = []
for v in range(0,len(lon_data)):
    origin = geopy.Point(lat_data[len(lat_data)-1],lon_data[v])
    destination = VincentyDistance(kilometers=Side_of_cell/2).destination(origin,270)
    lon_data_new.append(destination.longitude)

# Turn the lon/lat of the bins into 2 dimensional arrays ready
# for conversion into projected coordinates
lon_bins_2d, lat_bins_2d = np.meshgrid(lon_data_new,lat_data_new) 
# convert the bin mesh to map coordinates:
xs, ys = m(lon_bins_2d, lat_bins_2d) # will be plotted using pcolormesh    
density = np.reshape(chan_avl_cell,(dim,dim))

cmap = LinearSegmentedColormap.from_list('mycmap', ['palegoldenrod','orange','red'])
plt.pcolormesh(xs, ys, density,cmap=cmap,alpha = 0.8,linewidths=2)
cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
tick_locator = ticker.MaxNLocator(nbins=density.max())
cbar.locator = tick_locator
cbar.update_ticks()
plt.setp(cbar.ax.yaxis.get_ticklabels(), weight='bold', fontsize=15)
cbar.set_label('Number of channels', rotation=90,weight='bold', fontsize=20)

plt.tight_layout()
plt.savefig('Heatmap_channel_availability_Cell3f5km.png',dpi=300,bbox_inches='tight',pad = 1)
plt.show()
print datetime.now() - startTime