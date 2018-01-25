# TVWS-Database
This database has been compiled for our work "Optimizing City-Wide Wi-Fi networks in TV white spaces". Below pointers may be helpful in understanding the database.

1. TV_TOWER_DATA.csv has information related to TV networks for the United States.
2. The csv file has data combined from tv_eng_data.zip available at https://www.fcc.gov/media/radio/cdbs-database-public-files and TV_service_contour_current.zip available https://www.fcc.gov/media/television/tv-service-contour-data-points.

While FCC provides only the service contour points of any TV transmitter, we have generated the protected contour points for every TV transmitter by following the guidelines in http://spectrumbridge.com/wp-content/uploads/2014/08/Database-Calculation-Consistency-Specification.pdf.

We use this database to compute channel availability and verify it with the information at https://spectrum.iconectiv.com/main/home/contour_vis.shtml. 

Miscellaneous links:
    (a) To understand the concept of Grade A and Grade B contour, please see "Understanding television’s Grade A and Grade B Service contours" (http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=969381). 
    (b) To know the details of database calculations, please see http://spectrumbridge.com/wp-content/uploads/2014/08/Database-Calculation-Consistency-Specification.pdf. 
    (c) To study classes of TV transmitters and Grade A and Grade B contours, please see https://www.fcc.gov/media/radio/fm-station-classes










