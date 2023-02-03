import os
import libpysal
import geopandas as gpd
from itertools import groupby

districts_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/GIS/116/US_cd116th_2021.shp"
counties_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/county_gis_data/county_data_2022/tl_2022_us_county.shp"

congressional_districts= gpd.read_file(districts_path)
counties= gpd.read_file(counties_path)

result= libpysal.spatial_join(counties, congressional_districts)

grouped= groupby(result, lambda x: x[1])

counts= {congressional_district: len(list(counties)) for congressional_district, counties in grouped}

print(counts)

