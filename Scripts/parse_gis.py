import os
import libpysal
import geopandas as gpd
from itertools import groupby
from shapely.geometry import Polygon
import json



districts_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/GIS/116/US_cd116th_2021.shp"
counties_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/county_gis_data/county_data_2022/tl_2022_us_county.shp"

districts= gpd.read_file(districts_path)
counties= gpd.read_file(counties_path)

#creating the district id number by concatinating the STATEFP
#and the CD116FP values, separated by a "-"
districts['STATEFP']= districts['STATEFP'].astype(str)
districts['CD116FP']= districts['CD116FP'].astype(str)
districts['district_id']= districts['STATEFP']+ '-' + districts['CD116FP']

#creating county_id values via same method
counties['STATEFP']= counties['STATEFP'].astype(str)
counties['COUNTYFP']= counties['COUNTYFP'].astype(str)
counties['county_id']= counties['STATEFP']+ '-' + counties['COUNTYFP']

overlap_dict= {}

#ensuring the CRS type of both Shapefiles are the same
#rescaling the county, shapefile if they are different

districts= districts.to_crs(5070)
counties= counties.to_crs(5070)

#getting rid of invalid geometries such as
#polygons that intersect themselves, 
counties['geometry'].buffer(0)
districts['geometry'].buffer(0)

for i, row1 in districts.iterrows():
    district_id= row1['district_id']
    district_polygon= row1['geometry']

    overlap_df= gpd.GeoDataFrame({'geometry': [Polygon()]})
    overlap_df.crs= districts.crs

    state= row1['STATEFP']
    county_valid= counties[counties['STATEFP'] == state]

    for j, row2 in county_valid.iterrows():

        county_id= row2['county_id']
        county_polygon= row2['geometry']

        overlap= district_polygon.intersection(district_polygon)

        overlap_df= overlap_df.append({'geometry': overlap, "district_id": county_id}, ignore_index = True)

        overlap_df['area_ratio']= (overlap_df.geometry.area / county_polygon.area)

    overlap_grouped= overlap_df.groupby(['district_id']).sum()

    for district_id, overlap_ratio in zip(overlap_grouped.index, overlap_grouped['area_ratio']):
        overlap_dict[county_id, district_id]= overlap_ratio



with open('output.txt', 'w') as f:
    f.write(json.dumps(overlap_dict))

    