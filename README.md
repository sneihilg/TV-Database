# TVWS-Database
This database has been compiled for our work "Optimizing City-Wide Wi-Fi networks in TV white spaces". Below pointers may be helpful in understanding the database.

1. TV_TOWER_DATA.csv has information related to TV networks and the predicted service contour points for each TV transmitter.
2. The csv has data combined from tv_eng_data.zip available at https://www.fcc.gov/media/radio/cdbs-database-public-files and TV_service_contour_current.zip available https://www.fcc.gov/media/television/tv-service-contour-data-points.
3. Use https://www.fcc.gov/media/radio/fm-station-classes for information on classes of TV transmitters and Grade A and Grade B contours.
5. To understand the concept of Grade A and Grade B contour see "Understanding television’s Grade A and Grade B Service contours" (http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=969381).
6. Choice of separation distance http://spectrumbridge.com/wp-content/uploads/2014/08/Database-Calculation-Consistency-Specification.pdf.

While FCC provides only the service contour points of a TV transmitter, we have created the protected region for every TV TX by following the guidelines in http://spectrumbridge.com/wp-content/uploads/2014/08/Database-Calculation-Consistency-Specification.pdf and have added to the TV_TOWER_DATA.csv.

Further, we use this database to compute channel availability and verify it with the information at https://spectrum.iconectiv.com/main/home/contour_vis.shtml. 




