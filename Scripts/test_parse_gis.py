import geopandas as gpd
import shapely.geometry
import os
import itertools
import pandas as pd

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

counties.crs = {'init': 'epsg:4326'}
districts.crs = {'init': 'epsg:4326'}

districts['geometry'].buffer(0)
counties['geometry'].buffer(0)

def calculate_overlap(counties_gdf, districts_gdf):
    districts_gdf = districts_gdf.copy()
    districts_gdf['overlap'] = districts_gdf.apply(lambda x: [], axis=1)
    
    for district in districts_gdf.itertuples():
        district_polygon = district.geometry
        for county in counties_gdf.itertuples():
            county_polygon = county.geometry
            if county_polygon.within(district_polygon):
                overlap = 1.0
            else:
                overlap = district_polygon.intersection(county_polygon).area / district_polygon.area
                
                if overlap > 0:
                    districts_gdf.at[district.Index, 'overlap'].append({county.county_id: overlap})
    
    return districts_gdf


result= calculate_overlap(counties, districts)

print(result['overlap'])