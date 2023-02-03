import os
import libpysal
import geopandas as gpd
from itertools import groupby
from shapely.geometry import Polygon

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

for i, row1, in counties.iterrows():
    county_id= row1['county_id']
    county_polygon= row1['geometry']

    if not county_polygon.is_valid:
        print(f'INVALID GEOMETRY FOUND!: COUNTIES INDEX = {i}')
        input()
    
    overlap_df= gpd.GeoDataFrame({'geometry': [Polygon()]})
    overlap_df.crs= districts.crs

    for j, row2 in districts.iterrows():
        district_id= row2['district_id']
        district_polygon= row2['geometry']
        
        if not district_polygon.is_valid:
            print(f'INVALID GEOMETRY FOUND!: DISTRICTS INDEX {j}')
            print(districts.at[j, 'district_id'])
            districts.at[j, 'geometry']= district_polygon.buffer(0)
            input()

        overlap= county_polygon.intersection(district_polygon)

        if not overlap.is_empty and not district_polygon.is_empty and not county_polygon.is_empty:
            overlap_df= overlap_df.append({'geometry': overlap, 'district_id': district_id}, ignore_index= True)

    overlap_df['area_ratio']= (overlap_df.geometry.area / county_polygon.area)

    overlap_grouped= overlap_df.groupby(['district_id']).sum()

    for district_id, overlap_ratio in zip(overlap_grouped.index, overlap_grouped['area_ratio']):
        overlap_dict[county_id, district_id]= overlap_ratio


print(overlap_dict.keys())




