# Date: 2-Dec-2016
# Code to generate data required for simulation setup
# We need (a) coordinates of each cell (b) Closest Primary transmitter on each available channel (c) Worst case receiver location
# on the service contour

import numpy as np 
import pandas as pd
import geopy
import json
from geopy.distance import VincentyDistance
from geopy.distance import vincenty
from shapely.geometry import Polygon, Point, LinearRing

from datetime import datetime
startTime = datetime.now()

Side_of_cell = 3.5
P_total = 0.1

Data = json.load(open('GradeB_SepDis_Denver_%.1fkm2Cell_Irregular_Sec70X70km2.json'%(Side_of_cell),'r'))

def Pri_rx_loc(poly_data,point_data):
    poly = Polygon(poly_data)
    point = Point(point_data)    
    pol_ext = LinearRing(poly.exterior.coords)
    d = pol_ext.project(point)
    p = pol_ext.interpolate(d)
    closest_point_coords = list(p.coords)[0]
    closest_point_dis = vincenty(point_data,closest_point_coords).miles*1.60934
    return closest_point_coords,closest_point_dis
    
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
center = []
Cell_coord = []
TV_Tower_Dist = []
TV_Tower_Loc = []
TV_HAAT_Data = []
TV_ERP_Data = []
TV_Chan = []
TV_Receiver_Dist = []
TV_Receiver_Loc = []
bear_degree = [45,135,225,315]
out_channels = {}
for cell in range(0,len(Data)):
    CENTER = (Data[str(cell)]['location'][1],Data[str(cell)]['location'][0])
    dis = ((2*(Side_of_cell**2))**0.5)/2
    orig = geopy.Point(CENTER[0],CENTER[1])
    val = []
    for b in range(0,len(bear_degree)):
        destination = VincentyDistance(kilometers=dis).destination(orig,bear_degree[b])
        lat = destination.latitude
        lon = destination.longitude
        ext = (lat,lon)
        val.extend([ext])
    Cell_coord.append(val) 
    chan_avl = (Data[str(cell)]['Available_channel'])
    TV_chan = []
    TV_TX_Dist = []
    TV_TX_loc = []
    TV_haat = []
    TV_erp = []
    TV_RX_Dist = []
    TV_RX_loc = []
    for count_chan in range(0,len(chan_avl)):
        Distance = []
        TV_TX = []
        TV_TX_cont = []
        TV_RX = []
        HAAT = []
        ERP = []
        Rx_worst_coord = []
        Rx_worst_dis = []
        for row in range(0,len(df)):
            channel_no = df.ix[row]['station_channel']
            if chan_avl[count_chan]==channel_no:
                TV_Tower = (df.ix[row]['Latitude'],df.ix[row]['Longitude'])
                TV_HAAT = df.ix[row]['HAAT_m']
                TV_ERP = df.ix[row]['effective_erp']
                TV_service_contour = poly_overall[row]
                Dist = []
                Rec_coords = []
                Rec_dis = []
                for vertex in range(0,len(Cell_coord[cell])):
                    # For worst case receiver for a cell, pick the receiver from each vertex, select the closest receiver
                    poly_data = poly_overall[row]
                    point_data = Cell_coord[cell]
                    (Rx_coords,Rx_dis) = Pri_rx_loc(poly_data,point_data[vertex])
                    Rec_coords.append(Rx_coords)
                    Rec_dis.append(Rx_dis)
                    Dist.append(vincenty(TV_Tower,Cell_coord[cell][vertex]).miles*1.60934)
                Rx_min_dis = np.min(Rec_dis)        
                Rx_min_Index = [i for i, x in enumerate(Rec_dis) if x == Rx_min_dis]
                Index = Rx_min_Index[0]
                Rx_worst_coord.append(Rec_coords[Index])
                Rx_worst_dis.append(Rec_dis[Index])
                Value = min(Dist)
                Distance.append(Value)
                TV_TX.append(TV_Tower)
                HAAT.append(TV_HAAT)
                ERP.append(TV_ERP)
        TV_RX_Dist.append(Rx_worst_dis)
        TV_RX_loc.append(Rx_worst_coord)
        TV_TX_Dist.append(Distance)
        TV_TX_loc.append(TV_TX)
        TV_haat.append(HAAT)
        TV_erp.append(ERP)
        TV_chan.append(chan_avl[count_chan])
    TV_Chan.append(TV_chan)
    TV_Tower_Dist.append(TV_TX_Dist)
    TV_Tower_Loc.append(TV_TX_loc)
    TV_Receiver_Dist.append(TV_RX_Dist)
    TV_Receiver_Loc.append(TV_RX_loc)
    TV_HAAT_Data.append(TV_haat)
    TV_ERP_Data.append(TV_erp)
    out = {"cell_center":(Data[str(cell)]['location'][1],Data[str(cell)]['location'][0]),
       "cell_coord":Cell_coord[cell],
       "num_chan_aval":len(chan_avl),
       "chan_available":(TV_Chan[cell]),
       "TV_TX_Loc":(TV_Tower_Loc[cell]),
       "TV_TX_Dist":(TV_Tower_Dist[cell]),
       "TV_Tower_HAAT":(TV_HAAT_Data[cell]),
       "TV_Tower_ERP":(TV_ERP_Data[cell]),
       "TV_RX_Loc":(TV_Receiver_Loc[cell]),
       "TV_RX_Dist":(TV_Receiver_Dist[cell]),
       "Origin_xy":(Data[str(cell)]['Origin_xy'])}
    out_channels[cell] = out
json.dump(out_channels, open('GrdB_Denver_SepDis_%.1fkm2_Sim_Setup_Sec70X70km2.json'%(Side_of_cell),'w')) 


Data = json.load(open('GrdB_Denver_SepDis_%.1fkm2_Sim_Setup_Sec70X70km2.json'%(Side_of_cell),'r'))

def find_rx_dis(RX_coord,cells_with_chan):
    for cell in range (0,len(cells_with_chan)):
        Cell_coord = Data[str(cells_with_chan[cell])]['cell_coord']
        Dist = []
        for vertex in range(0,len(Cell_coord)):
            Dist.append(vincenty(RX_coord,Cell_coord[vertex]).miles*1.60934)
        RX_min_cell = np.min(Dist)
        Rx_dis.append(RX_min_cell)
    return Rx_dis

#find all available channels across area
channel_avl = []
for cell in range(0,len(Data)):
    channel_avl.extend(Data[str(cell)]['chan_available'])
channel_avl = sorted(list(set(channel_avl)))

# find cell_nos with channel available and also total number of primary networks operating on the available channels
cell_chan = []          # cell number operating on an available channel
cell_num_pri = []       # number of primary networks operating on the available chanel
for num_chan_avl in range(0,len(channel_avl)):
    cell_with_chan = []
    num_pri_on_chan = []
    for cell in range(0,len(Data)):
        chan = Data[str(cell)]['chan_available']
        if channel_avl[num_chan_avl] in chan:
            INDEX = chan.index(channel_avl[num_chan_avl])
            TV_Rx = Data[str(cell)]['TV_RX_Loc'][INDEX]
            num_pri_on_chan.append(len(TV_Rx))
            cell_with_chan.append(cell)
    cell_chan.append(cell_with_chan)
    cell_num_pri.extend(list(set(num_pri_on_chan)))

# For a channel: For each cell, we have a list of worst case receivers for all primary networks. Find the distance of the 
# the worst case receiver to the remaining cells. 
RX_Each_Chan_DIS = []
for num_chan_avl in range(0,len(channel_avl)):
    RX_Each_Cell_DIS = []
    for cell in range(0,len(cell_chan[num_chan_avl])):
        Cell = cell_chan[num_chan_avl][cell]
        chan = Data[str(Cell)]['chan_available']
        if channel_avl[num_chan_avl] in chan:
            INDEX = chan.index(channel_avl[num_chan_avl])
            TV_Rx = Data[str(Cell)]['TV_RX_Loc'][INDEX]
            RX_DIS = []
            for num_rx in range(0,len(TV_Rx)):
                Rx_dis = []
                Rx_dis = find_rx_dis(TV_Rx[num_rx],cell_chan[num_chan_avl])
                RX_DIS.append(Rx_dis)
        RX_Each_Cell_DIS.append(RX_DIS)
    RX_Each_Chan_DIS.append(RX_Each_Cell_DIS)       # Note: RX_Each_Chan_DIS[num_chan_index][cell_no][RX_no] value has distance from RX to all cells that see chan[num_chan_index] available

# Short down the list of worst case receivers for a transmitter to a single worst case receiver
Worst_Case_RX_loc = []
Worst_Case_RX_dis = []
for num_chan_avl in range(0,len(channel_avl)):
    Worst_RX_loc = []    
    Worst_RX_dis = []
    for num_pri in range(0,cell_num_pri[num_chan_avl]):
        RX_Val = []
        RX_index = []
        for cell in range(0,len(cell_chan[num_chan_avl])):
            Cell = cell_chan[num_chan_avl][cell]
            chan = Data[str(Cell)]['chan_available']
            if channel_avl[num_chan_avl] in chan:
                INDEX = chan.index(channel_avl[num_chan_avl])
                RX_Val.append(RX_Each_Chan_DIS[num_chan_avl][cell][num_pri])
                RX_index.append(INDEX)
        RX_VAL = np.multiply(np.divide(1,np.power(np.asmatrix(RX_Val),3)),P_total)
        size_of_rx = RX_VAL.shape
        Total_int = [sum(RX_VAL[:,i]) for i in range(int(size_of_rx[0]))]
#        find the index that causes maximum interference
        Index_RX = np.argmax(Total_int)
        Index_chan = RX_index[Index_RX]
        Index_cell = cell_chan[num_chan_avl][Index_RX]
        Index_cell_cell_chan = cell_chan[num_chan_avl].index(Index_cell)
        Rx_loc_data = Data[str(Index_cell)]['TV_RX_Loc'][Index_chan][num_pri]
        RX_dis = RX_Each_Chan_DIS[num_chan_avl][Index_cell_cell_chan][num_pri]
        Worst_RX_loc.append(Rx_loc_data)
        Worst_RX_dis.append(RX_dis)
    Worst_Case_RX_loc.append(Worst_RX_loc)
    Worst_Case_RX_dis.append(Worst_RX_dis)

out_channels = {}
for cell in range(0,len(Data)):
    TV_Receiver_Loc = []
    TV_Receiver_Dist = []
    Cell_center = Data[str(cell)]['cell_center']
    Cell_coord = Data[str(cell)]['cell_coord']
    chan_avl = Data[str(cell)]['num_chan_aval']
    TV_Chan = Data[str(cell)]['chan_available']
    TV_Tower_Loc = Data[str(cell)]['TV_TX_Loc']
    TV_Tower_Dist = Data[str(cell)]['TV_TX_Dist']
    TV_HAAT_Data = Data[str(cell)]['TV_Tower_HAAT']
    TV_ERP_Data = Data[str(cell)]['TV_Tower_ERP']
    for num_chan_avl in range(0,len(channel_avl)):
        if channel_avl[num_chan_avl] in TV_Chan:
            TV_Receiver_Loc.append(Worst_Case_RX_loc[num_chan_avl])
            TV_Receiver_Dist.append(Worst_Case_RX_dis[num_chan_avl])
    out = {"cell_center":Cell_center,
           "cell_coord":Cell_coord,
           "num_chan_aval":chan_avl,
           "chan_available":(TV_Chan),
           "TV_TX_Loc":(TV_Tower_Loc),
           "TV_TX_Dist":(TV_Tower_Dist),
           "TV_Tower_HAAT":(TV_HAAT_Data),
           "TV_Tower_ERP":(TV_ERP_Data),
           "TV_RX_Loc":(TV_Receiver_Loc),
           "TV_RX_Dist":(TV_Receiver_Dist),
           "Origin_xy":(Data[str(cell)]['Origin_xy'])}
    out_channels[cell] = out
json.dump(out_channels, open('GrdB_Denver_SepDis_%.1fkm2_Sim_Data_Sec_70X70km2.json'%(Side_of_cell),'w')) 
print datetime.now() - startTime