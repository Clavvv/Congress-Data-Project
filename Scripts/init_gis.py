import os
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement
import pandas as pd
import geopandas as gpd
import json
import glob
#from parse_gis import match


def init_gis():

    dir_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    #Reading and parsing json to populate db connection credentials
    params= json.load(open(dir_path+"\GIS_DB.json"))
    user= params['username']
    pwd= params['password']
    host= params['host']
    port= params['socket']
    database= params['database']

    #creating database connection engine
    engine= create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{database}')

    #getting filepaths for shapefiles
    gis_path= f"{dir_path}/GIS"
    gis_files= glob.glob(f"{gis_path}/**/*.shp", recursive=True)

    for file in gis_files:
        
        #cleaning the file path strings to use as table names
        table_name= file.split(gis_path)
        table_name= table_name[1][1:].split('_', 1)
        table_name= table_name[1]

        #read in shapefile as gdf
        gdf= gpd.read_file(file)
        
        #creating table and uploading to PostGIS
        gdf.to_postgis(con= engine, name= table_name, if_exists= 'replace', schema= 'public')


if __name__ == "__main__":
    init_gis()