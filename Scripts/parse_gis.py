import os
import geopandas as gpd
import shapely
import warnings 
import matplotlib.pyplot as plt
import itertools


warnings.simplefilter(action='ignore', category=FutureWarning)

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

#insuring CRS types are equivalent
if districts.crs != counties.crs:
    counties= counties.to_crs(districts.crs)


def get_overlap(layer1, layer2):

    assert layer1.crs == layer2.crs, "Layers must be of the same CRS format"


    join= gpd.sjoin(row, layer2, op='overlap')
    print(join.head())
    input()





    return overlap_json





if __name__ == "__main__":
    test= counties[counties['STATEFP'] == '01']
    test2= districts[districts['STATEFP'] == '01']

    get_overlap(test, test2)